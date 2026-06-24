"""
The orchestrator is the "team coordination" layer:
  1. A background scheduler thread continuously pulls queued tasks and
     hands them to a thread pool (bounded by the concurrency setting),
     which is how tasks keep completing even while the user is doing
     something else in the app (or the window is in the background).
  2. run_task() is the actual multi-agent pipeline for one task: the
     Coordinator plans subtasks, each subtask is routed to the right
     role, and outputs are saved as real files in the project folder.
"""
import json
import re
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor

from . import storage, ollama_client, web_search, doc_writer
from .agents import ROLES

_executor = None
_executor_size = None
_scheduler_started = False
_inflight = set()
_inflight_lock = threading.Lock()


def _get_executor():
    global _executor, _executor_size
    size = int(storage.get_settings().get("concurrency", "2"))
    if _executor is None or _executor_size != size:
        _executor_size = size
        _executor = ThreadPoolExecutor(max_workers=max(1, size))
    return _executor


def start_scheduler():
    global _scheduler_started
    if _scheduler_started:
        return
    _scheduler_started = True

    def loop():
        while True:
            try:
                _tick()
            except Exception:
                traceback.print_exc()
            time.sleep(1.5)

    t = threading.Thread(target=loop, daemon=True)
    t.start()


def _tick():
    limit = int(storage.get_settings().get("concurrency", "2"))
    with _inflight_lock:
        running = len(_inflight)
        slots = max(0, limit - running)
        if slots == 0:
            return
        queued = storage.list_queued_tasks()
        to_start = [tid for tid in queued if tid not in _inflight][:slots]
        for tid in to_start:
            _inflight.add(tid)
    for tid in to_start:
        _get_executor().submit(_run_and_release, tid)


def _run_and_release(task_id):
    try:
        run_task(task_id)
    finally:
        with _inflight_lock:
            _inflight.discard(task_id)


FILE_BLOCK_RE = re.compile(
    r"<<<FILE:\s*(?P<name>[^\n>]+?)\s*>>>\n(?P<body>.*?)(?:\n<<<END FILE>>>|\Z)",
    re.DOTALL,
)


def _extract_files(text: str):
    files = []
    for m in FILE_BLOCK_RE.finditer(text or ""):
        files.append((m.group("name").strip(), m.group("body").strip()))
    return files


def _strip_file_blocks(text: str):
    return FILE_BLOCK_RE.sub("", text or "").strip()


SEARCH_CAPABLE_ROLES = {"researcher", "analyst", "economist", "scientist"}


def _call_role(role_key: str, user_prompt: str, models: dict, images: list = None) -> str:
    role = ROLES[role_key]
    model = models.get(role["settings_key"], "")
    if not model:
        raise ollama_client.OllamaError(f"No model configured for role '{role_key}'")
    return ollama_client.chat(model=model, system=role["system"], user=user_prompt, images=images)


def _parse_plan(raw: str):
    raw = raw.strip()
    # Strip accidental markdown fences
    raw = re.sub(r"^```(json)?", "", raw).strip()
    raw = re.sub(r"```$", "", raw).strip()
    try:
        plan = json.loads(raw)
        if isinstance(plan, list) and plan:
            cleaned = []
            for item in plan:
                role = str(item.get("role", "")).lower().strip()
                instr = str(item.get("instruction", "")).strip()
                title = str(item.get("title", "")).strip()
                if role == "specialist" and instr and title:
                    cleaned.append({"role": "specialist", "title": title, "instruction": instr})
                elif role in ROLES and instr:
                    cleaned.append({"role": role, "instruction": instr})
            if cleaned:
                return cleaned
    except Exception:
        pass
    # Fallback: no usable plan -> route to a generalist, then proofreader,
    # so the task still makes progress regardless of topic/domain.
    return [
        {"role": "analyst", "instruction": raw},
        {"role": "proofreader", "instruction": "Proofread and finalize the above."},
    ]


def run_task(task_id: int):
    task = storage.get_task(task_id)
    if not task:
        return
    project_id = task["project_id"]
    storage.update_task_status(task_id, "running")
    storage.add_log(task_id, "system", "Task started.")

    settings = storage.get_settings()
    all_attachments = storage.get_attachments(task_id)
    image_attachments = [a for a in all_attachments if a["content"].startswith("IMAGE_BASE64::")]
    text_attachments = [a for a in all_attachments if not a["content"].startswith("IMAGE_BASE64::")]

    parent_context = None
    if task.get("parent_task_id"):
        parent = storage.get_task(task["parent_task_id"])
        if parent:
            parent_logs = storage.get_logs(task["parent_task_id"])
            transcript = "\n".join(
                f"[{l['role']}] {l['message']}" for l in parent_logs
                if l["role"] not in ("system",) and l["message"]
            )
            parent_context = (
                f"This is a FOLLOW-UP to an earlier task in this thread.\n"
                f"Earlier task: {parent['description']}\n\n"
                f"Earlier conversation/work (for context -- don't redo it, build on it):\n"
                f"{transcript[:6000]}"
            )

    try:
        # 0. If images were attached, describe them with a vision model
        # first, so every other role (none of which can see images) gets
        # a textual description to work from instead of a useless wall of
        # base64.
        image_descriptions = []
        if image_attachments:
            vision_model = settings.get("model_vision")
            if vision_model:
                storage.add_log(task_id, "vision", f"Looking at {len(image_attachments)} attached image(s)...")
                b64_list = [a["content"][len("IMAGE_BASE64::"):] for a in image_attachments]
                try:
                    description = _call_role(
                        "vision",
                        f"Task context: {task['description']}\n\nDescribe the attached image(s).",
                        settings,
                        images=b64_list,
                    )
                    storage.add_log(task_id, "vision", description)
                    image_descriptions.append(description)
                except ollama_client.OllamaError as e:
                    storage.add_log(
                        task_id, "vision",
                        f"Could not analyze the image(s): {e}\n"
                        f"(Make sure a vision-capable model is pulled, e.g.: ollama pull {vision_model})"
                    )
            else:
                storage.add_log(task_id, "vision", "Images were attached but no vision model is configured in Settings.")

        # 1. Coordinator plans the work
        storage.add_log(task_id, "coordinator", "Planning subtasks...")
        coordinator_prompt = task["description"]
        if parent_context:
            coordinator_prompt = parent_context + f"\n\nNew follow-up request:\n{task['description']}"
        if text_attachments:
            names = ", ".join(a["filename"] for a in text_attachments)
            coordinator_prompt += f"\n\n(The user attached these reference files: {names}. Plan steps that make use of them where relevant.)"
        if image_descriptions:
            coordinator_prompt += (
                f"\n\n(An image was attached and already analyzed by the Vision "
                f"specialist -- description: {image_descriptions[0][:500]}. "
                "Plan steps that use this description directly; this does not "
                "need research or web search, just someone to relay/use what "
                "was already seen.)"
            )
        plan_raw = _call_role("coordinator", coordinator_prompt, settings)
        storage.add_log(task_id, "coordinator", plan_raw)
        plan = _parse_plan(plan_raw)

        context_parts = [f"Original task:\n{task['description']}"]
        if parent_context:
            context_parts.insert(0, parent_context)
        if text_attachments:
            att_text = "\n\n".join(
                f"--- Attached file: {a['filename']} ---\n{a['content']}" for a in text_attachments
            )
            context_parts.append(f"Attached reference files provided by the user:\n{att_text}")
        if image_descriptions:
            context_parts.append(
                "An image WAS attached to this task and has already been analyzed "
                "by the team's Vision specialist (you cannot see it yourself, only "
                "this description). Base your response on this description -- do "
                "not claim no image was provided, and do not search the web or "
                "speculate generically about how image-analysis tools work; just "
                "use what was actually seen:\n" + "\n".join(image_descriptions)
            )
        all_files = {}  # filename -> latest content

        for step in plan:
            role_key = step["role"]
            instruction = step["instruction"]
            display_label = step["title"] if role_key == "specialist" else role_key
            storage.add_log(task_id, display_label, f"Working on: {instruction}")

            context = "\n\n---\n\n".join(context_parts)
            prompt = (
                f"Context so far:\n{context}\n\n"
                f"Your instruction:\n{instruction}\n\n"
                f"Known files so far: {', '.join(all_files.keys()) or '(none yet)'}"
            )

            wants_search = (role_key in SEARCH_CAPABLE_ROLES or role_key == "specialist") and not image_attachments
            if settings.get("web_research_enabled") == "true" and wants_search:
                storage.add_log(task_id, display_label, "Searching the web for current information...")
                results = web_search.search_web(instruction, max_results=4)
                if results:
                    search_block = "\n".join(
                        f"- {r['title']}: {r['snippet']} ({r['url']})" for r in results
                    )
                    prompt = f"Live web search results just fetched for this step:\n{search_block}\n\n" + prompt
                else:
                    storage.add_log(task_id, display_label, "Web search returned nothing useful; proceeding without it.")

            try:
                if role_key == "specialist":
                    title = step["title"]
                    model = settings.get("model_specialist") or settings.get("model_researcher")
                    if not model:
                        raise ollama_client.OllamaError("No model configured for specialist roles")
                    system = (
                        f"You are a professional {title}, a deep subject-matter expert in "
                        "that field. Apply that specific expertise to the instruction given, "
                        "the same way any specialist team member would for their own domain. "
                        "Be concrete and practical, and note any limits of what can be "
                        "assessed without hands-on/real-world access."
                    )
                    output = ollama_client.chat(model=model, system=system, user=prompt)
                else:
                    output = _call_role(role_key, prompt, settings)
            except ollama_client.OllamaError as e:
                storage.add_log(task_id, display_label, f"ERROR: {e}")
                storage.update_task_status(task_id, "failed", str(e))
                return

            storage.add_log(task_id, display_label, output)

            new_files = _extract_files(output)
            for name, content in new_files:
                all_files[name] = content

            summary_text = _strip_file_blocks(output)
            context_parts.append(
                f"[{display_label} output]\n"
                + (summary_text if summary_text else f"(updated files: {', '.join(n for n, _ in new_files)})")
            )

        # Save all produced files to disk + DB. If a filename ends in
        # .docx/.xlsx/.pptx, convert the team's text output into a real
        # native Office file instead of saving raw text under that
        # extension (which Word/Excel/PowerPoint couldn't open correctly).
        for name, content in all_files.items():
            binary, converted = doc_writer.convert_if_needed(name, content)
            if converted and binary is not None:
                storage.add_log(task_id, "system", f"Generated native file: {name}")
                storage.save_file(task_id, project_id, name, binary)
            else:
                storage.save_file(task_id, project_id, name, content)

        final_summary = context_parts[-1] if context_parts else "Task complete."
        if all_files:
            final_summary += "\n\nFiles produced: " + ", ".join(all_files.keys())

        storage.add_log(task_id, "system", "Task complete.")
        storage.update_task_status(task_id, "done", final_summary)

    except Exception as e:
        traceback.print_exc()
        storage.add_log(task_id, "system", f"ERROR: {e}")
        storage.update_task_status(task_id, "failed", str(e))
