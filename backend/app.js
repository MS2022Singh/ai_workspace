const state = {
  projects: [],
  activeProjectId: null,
  tasks: [],
  activeTaskId: null,
  roles: {},
  settings: {},
  availableModels: [],
  selectedFiles: [],
  conversationMode: false,
  lastSeenTaskStatus: {}, // task id -> status, used to detect completion transitions
  editingTaskId: null, // set while an edit textarea is open, to avoid polling wiping it out
};

const ROLE_ORDER = [
  "coordinator", "coder", "reviewer", "documenter", "proofreader",
  "researcher", "analyst", "economist", "writer", "historian",
  "archaeologist", "scientist", "engineer", "vision",
];

async function api(path, opts) {
  const res = await fetch(path, opts);
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail.detail || `Request failed: ${path}`);
  }
  return res.json();
}

// ---------- error visibility ----------

function showError(message) {
  const banner = document.getElementById("error-banner");
  banner.innerHTML = "";
  const text = document.createElement("span");
  text.textContent = "⚠ " + message;
  const close = document.createElement("button");
  close.textContent = "×";
  close.onclick = () => banner.classList.add("hidden");
  banner.appendChild(text);
  banner.appendChild(close);
  banner.classList.remove("hidden");
}

window.addEventListener("error", (e) => showError(e.message || "Something went wrong."));
window.addEventListener("unhandledrejection", (e) =>
  showError((e.reason && e.reason.message) || "A background request failed.")
);

// ---------- voice input (local, offline transcription) ----------
// Deliberately NOT using the browser's built-in SpeechRecognition API --
// in Chrome/Edge that sends audio to a cloud service for processing,
// which would break this app's "stays on your machine" promise. Instead
// we capture raw PCM in the browser, build a WAV file ourselves, and send
// it to our own local backend, which transcribes it with a local offline
// model (Vosk). Nothing audio-related ever leaves this machine.

let micState = null; // { stream, audioContext, processor, samples: [], sampleRate }

function floatTo16BitPCM(float32Array) {
  const out = new Int16Array(float32Array.length);
  for (let i = 0; i < float32Array.length; i++) {
    const s = Math.max(-1, Math.min(1, float32Array[i]));
    out[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
  }
  return out;
}

function downsample(samples, fromRate, toRate) {
  if (toRate === fromRate) return samples;
  const ratio = fromRate / toRate;
  const newLength = Math.round(samples.length / ratio);
  const result = new Float32Array(newLength);
  for (let i = 0; i < newLength; i++) {
    result[i] = samples[Math.min(samples.length - 1, Math.round(i * ratio))];
  }
  return result;
}

function encodeWav(int16Samples, sampleRate) {
  const buffer = new ArrayBuffer(44 + int16Samples.length * 2);
  const view = new DataView(buffer);
  const writeStr = (offset, str) => {
    for (let i = 0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i));
  };
  writeStr(0, "RIFF");
  view.setUint32(4, 36 + int16Samples.length * 2, true);
  writeStr(8, "WAVE");
  writeStr(12, "fmt ");
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true); // PCM
  view.setUint16(22, 1, true); // mono
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * 2, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);
  writeStr(36, "data");
  view.setUint32(40, int16Samples.length * 2, true);
  let offset = 44;
  for (let i = 0; i < int16Samples.length; i++, offset += 2) {
    view.setInt16(offset, int16Samples[i], true);
  }
  return new Blob([view], { type: "audio/wav" });
}

async function startRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const audioContext = new (window.AudioContext || window.webkitAudioContext)();
  const source = audioContext.createMediaStreamSource(stream);
  const processor = audioContext.createScriptProcessor(4096, 1, 1);
  const samples = [];
  source.connect(processor);
  processor.connect(audioContext.destination);
  processor.onaudioprocess = (e) => {
    samples.push(new Float32Array(e.inputBuffer.getChannelData(0)));
  };
  micState = { stream, audioContext, processor, samples };
}

function stopRecordingAndBuildWav() {
  const { stream, audioContext, processor, samples } = micState;
  processor.disconnect();
  stream.getTracks().forEach((t) => t.stop());
  const sampleRateIn = audioContext.sampleRate;
  let total = 0;
  samples.forEach((s) => (total += s.length));
  const merged = new Float32Array(total);
  let o = 0;
  samples.forEach((s) => { merged.set(s, o); o += s.length; });
  audioContext.close();
  micState = null;
  const resampled = downsample(merged, sampleRateIn, 16000);
  const pcm16 = floatTo16BitPCM(resampled);
  return encodeWav(pcm16, 16000);
}

async function toggleMic() {
  const btn = document.getElementById("mic-btn");
  if (!micState) {
    try {
      await startRecording();
      btn.classList.add("recording");
      btn.textContent = "● Stop";
    } catch (e) {
      showError("Couldn't access the microphone: " + e.message);
    }
    return;
  }
  btn.classList.remove("recording");
  btn.textContent = "⏳ Transcribing...";
  try {
    const wavBlob = stopRecordingAndBuildWav();
    const formData = new FormData();
    formData.append("audio", wavBlob, "speech.wav");
    const res = await fetch("/api/voice/transcribe", { method: "POST", body: formData });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Transcription failed");
    const input = document.getElementById("task-input");
    input.value = (input.value.trim() + " " + data.text).trim();
    if (state.conversationMode && input.value.trim()) {
      await submitTask();
    }
  } catch (e) {
    showError(e.message);
  } finally {
    btn.textContent = "🎤 Voice";
  }
}

function toggleConversationMode() {
  state.conversationMode = !state.conversationMode;
  const btn = document.getElementById("conversation-btn");
  btn.classList.toggle("active", state.conversationMode);
  btn.textContent = "🔁 Conversation mode: " + (state.conversationMode ? "On" : "Off");
}

// ---------- universal downloads ----------
// Inside the embedded app window, the usual "hidden <a download> link"
// browser trick isn't reliable, so we hand bytes/text to Python, which
// shows a real native Save dialog. In browser mode (no pywebview bridge
// present), we fall back to the standard browser download mechanism.

function arrayBufferToBase64(buffer) {
  let binary = "";
  const bytes = new Uint8Array(buffer);
  const chunk = 0x8000;
  for (let i = 0; i < bytes.length; i += chunk) {
    binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
  }
  return btoa(binary);
}

function hasNativeSave() {
  return !!(window.pywebview && window.pywebview.api && window.pywebview.api.save_binary);
}

async function triggerBlobDownload(filename, blob) {
  if (hasNativeSave()) {
    const buf = await blob.arrayBuffer();
    const base64 = arrayBufferToBase64(buf);
    const result = await window.pywebview.api.save_binary(filename, base64);
    if (result && result.ok === false && !result.cancelled) {
      showError("Could not save file: " + (result.error || "unknown error"));
    }
    return;
  }
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

async function triggerTextDownload(filename, text) {
  if (window.pywebview && window.pywebview.api && window.pywebview.api.save_text) {
    const result = await window.pywebview.api.save_text(filename, text);
    if (result && result.ok === false && !result.cancelled) {
      showError("Could not save file: " + (result.error || "unknown error"));
    }
    return;
  }
  await triggerBlobDownload(filename, new Blob([text], { type: "text/plain" }));
}

async function downloadFromGet(url, filename) {
  try {
    const res = await fetch(url);
    if (!res.ok) {
      const detail = await res.json().catch(() => ({}));
      throw new Error(detail.detail || "Download failed");
    }
    await triggerBlobDownload(filename, await res.blob());
  } catch (e) {
    showError("Download failed: " + e.message);
  }
}

async function downloadFromPost(url, formData, filename) {
  try {
    const res = await fetch(url, { method: "POST", body: formData });
    if (!res.ok) {
      const detail = await res.json().catch(() => ({}));
      throw new Error(detail.detail || "Request failed");
    }
    await triggerBlobDownload(filename, await res.blob());
    return true;
  } catch (e) {
    showError(e.message);
    return false;
  }
}

// ---------- read-aloud (local OS voice, no network) ----------

function readAloud(text, btn) {
  if (!("speechSynthesis" in window)) {
    showError("Your browser doesn't support text-to-speech.");
    return;
  }
  if (window.speechSynthesis.speaking) {
    window.speechSynthesis.cancel();
    document.querySelectorAll(".read-aloud-btn.speaking").forEach((b) => b.classList.remove("speaking"));
    return;
  }
  const voices = window.speechSynthesis.getVoices();
  if (voices.length === 0) {
    showError(
      "No system voice is available for read-aloud yet (this can happen right " +
      "after starting the app). Try again in a few seconds, or check Windows " +
      "has a voice installed: Settings → Time & Language → Speech."
    );
    return;
  }
  const utter = new SpeechSynthesisUtterance(text);
  if (btn) btn.classList.add("speaking");
  utter.onend = () => { if (btn) btn.classList.remove("speaking"); };
  utter.onerror = (e) => {
    if (btn) btn.classList.remove("speaking");
    showError("Read-aloud failed: " + (e.error || "unknown error"));
  };
  window.speechSynthesis.speak(utter);
}

// ---------- main tabs ----------

function switchMainTab(tab) {
  document.getElementById("tab-tasks").classList.toggle("active", tab === "tasks");
  document.getElementById("tab-media").classList.toggle("active", tab === "media");
  document.getElementById("tasks-view").classList.toggle("hidden", tab !== "tasks");
  document.getElementById("media-view").classList.toggle("hidden", tab !== "media");
}

// ---------- media tools (deterministic, local image/video tools) ----------

const EDIT_PARAM_FIELDS = {
  resize: [["width", "Width (px)", 800], ["height", "Height (px)", 600]],
  crop: [["left", "Left", 0], ["top", "Top", 0], ["right", "Right", 400], ["bottom", "Bottom", 400]],
  rotate: [["degrees", "Degrees", 90]],
  blur: [["radius", "Blur radius", 4]],
  brightness: [["factor", "Factor (1.0 = unchanged)", 1.2]],
  contrast: [["factor", "Factor (1.0 = unchanged)", 1.2]],
};

function renderEditParams() {
  const op = document.getElementById("edit-operation").value;
  const wrap = document.getElementById("edit-params");
  wrap.innerHTML = "";
  const fields = EDIT_PARAM_FIELDS[op] || [];
  for (const [key, label, def] of fields) {
    const lbl = document.createElement("label");
    lbl.textContent = label;
    const input = document.createElement("input");
    input.type = "number";
    input.step = "any";
    input.id = `edit-param-${key}`;
    input.value = def;
    lbl.appendChild(input);
    wrap.appendChild(lbl);
  }
}

function bindMediaTools() {
  document.getElementById("tab-tasks").onclick = () => switchMainTab("tasks");
  document.getElementById("tab-media").onclick = () => switchMainTab("media");

  // --- collage / grid splitter ---
  document.getElementById("split-btn").onclick = async () => {
    const fileInput = document.getElementById("split-image-input");
    const status = document.getElementById("split-status");
    if (!fileInput.files.length) { status.textContent = "Choose an image first."; return; }
    const rows = document.getElementById("split-rows").value || "2";
    const cols = document.getElementById("split-cols").value || "2";
    const fd = new FormData();
    fd.append("image", fileInput.files[0]);
    fd.append("rows", rows);
    fd.append("cols", cols);
    status.textContent = "Splitting...";
    const ok = await downloadFromPost("/api/media/split-grid", fd, "split_images.zip");
    status.textContent = ok ? "Done -- check your save dialog / downloads." : "";
  };

  // --- image editor ---
  document.getElementById("edit-operation").onchange = renderEditParams;
  renderEditParams();
  document.getElementById("edit-btn").onclick = async () => {
    const fileInput = document.getElementById("edit-image-input");
    const status = document.getElementById("edit-status");
    if (!fileInput.files.length) { status.textContent = "Choose an image first."; return; }
    const op = document.getElementById("edit-operation").value;
    const fmt = document.getElementById("edit-format").value;
    const params = { format: fmt };
    for (const [key] of EDIT_PARAM_FIELDS[op] || []) {
      const el = document.getElementById(`edit-param-${key}`);
      if (el) params[key] = el.value;
    }
    const fd = new FormData();
    fd.append("image", fileInput.files[0]);
    fd.append("operation", op);
    fd.append("params", JSON.stringify(params));
    status.textContent = "Processing...";
    const ok = await downloadFromPost("/api/media/edit", fd, `edited.${fmt}`);
    status.textContent = ok ? "Done -- check your save dialog / downloads." : "";
  };

  // --- logo generator ---
  document.getElementById("logo-btn").onclick = async () => {
    const text = document.getElementById("logo-text").value.trim();
    const status = document.getElementById("logo-status");
    if (!text) { status.textContent = "Enter at least the main text."; return; }
    const subtext = document.getElementById("logo-subtext").value.trim();
    const palette = document.getElementById("logo-palette").value;
    const fd = new FormData();
    fd.append("text", text);
    fd.append("subtext", subtext);
    fd.append("palette", palette);
    status.textContent = "Generating...";
    try {
      const res = await fetch("/api/media/logo", { method: "POST", body: fd });
      if (!res.ok) {
        const detail = await res.json().catch(() => ({}));
        throw new Error(detail.detail || "Could not generate logo");
      }
      const blob = await res.blob();
      const preview = document.getElementById("logo-preview");
      preview.src = URL.createObjectURL(blob);
      preview.style.display = "block";
      await triggerBlobDownload("logo.png", blob);
      status.textContent = "Done -- check your save dialog / downloads.";
    } catch (e) {
      status.textContent = "";
      showError(e.message);
    }
  };

  // --- slideshow / reel ---
  document.getElementById("slideshow-btn").onclick = async () => {
    const filesInput = document.getElementById("slideshow-images-input");
    const status = document.getElementById("slideshow-status");
    if (!filesInput.files.length) { status.textContent = "Choose at least one image."; return; }
    const seconds = document.getElementById("slideshow-seconds").value || "2";
    const format = document.getElementById("slideshow-format").value;
    const fd = new FormData();
    for (const f of filesInput.files) fd.append("images", f);
    fd.append("seconds_per_slide", seconds);
    fd.append("output_format", format);
    status.textContent = "Creating slideshow (this can take a little while)...";
    const ok = await downloadFromPost("/api/media/slideshow", fd, `slideshow.${format}`);
    status.textContent = ok ? "Done -- check your save dialog / downloads." : "";
  };
}

// ---------- bootstrap ----------

async function init() {
  bindEvents();
  if ("speechSynthesis" in window) {
    window.speechSynthesis.getVoices(); // kick off async loading early
    window.speechSynthesis.onvoiceschanged = () => window.speechSynthesis.getVoices();
  }
  try {
    await refreshHealth();
    state.roles = await api("/api/roles");
    state.settings = await api("/api/settings");
    await refreshProjects();
    renderRoster();
    setInterval(refreshHealth, 8000);
    setInterval(refreshActiveProjectTasks, 2000);
    setInterval(refreshActiveTaskDetail, 2000);
  } catch (e) {
    showError("Failed to start: " + e.message);
  }
}

async function refreshHealth() {
  try {
    const h = await api("/api/health");
    const el = document.getElementById("ollama-status");
    if (h.ollama_running) {
      el.textContent = "engine online";
      el.className = "brand-sub ok";
    } else {
      el.textContent = "Ollama not detected";
      el.className = "brand-sub bad";
    }
  } catch (e) {
    const el = document.getElementById("ollama-status");
    el.textContent = "engine unreachable";
    el.className = "brand-sub bad";
  }
}

// ---------- projects ----------

async function refreshProjects() {
  state.projects = await api("/api/projects");
  if (!state.projects.length) {
    // Don't make the person create a project before they can do anything --
    // give them a default one transparently. They can still rename/add more
    // later if they want to organize work into separate projects.
    const { id } = await api("/api/projects", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: "General" }),
    });
    state.projects = await api("/api/projects");
    state.activeProjectId = id;
  }
  renderProjectList();
  if (!state.activeProjectId) {
    selectProject(state.projects[0].id);
  } else {
    await refreshActiveProjectTasks();
    const p = state.projects.find((x) => x.id === state.activeProjectId);
    if (p) {
      document.getElementById("active-project-label").textContent = "Project";
      document.getElementById("active-project-name").textContent = p.name;
    }
  }
}

function renderProjectList() {
  const list = document.getElementById("project-list");
  list.innerHTML = "";
  if (!state.projects.length) {
    const empty = document.createElement("div");
    empty.className = "hint";
    empty.style.padding = "6px 4px";
    empty.textContent = "No projects yet.";
    list.appendChild(empty);
    return;
  }
  for (const p of state.projects) {
    const item = document.createElement("div");
    item.className = "project-item" + (p.id === state.activeProjectId ? " active" : "");
    const nameSpan = document.createElement("span");
    nameSpan.textContent = p.name;
    nameSpan.style.flex = "1";
    const delBtn = document.createElement("button");
    delBtn.className = "row-delete-btn";
    delBtn.textContent = "×";
    delBtn.title = "Delete project and all its tasks";
    delBtn.onclick = async (e) => {
      e.stopPropagation();
      if (!confirm(`Delete project "${p.name}" and all its tasks? This can't be undone.`)) return;
      await api(`/api/projects/${p.id}`, { method: "DELETE" });
      if (state.activeProjectId === p.id) {
        state.activeProjectId = null;
        state.activeTaskId = null;
      }
      await refreshProjects();
      renderTaskDetailEmpty();
    };
    item.style.display = "flex";
    item.appendChild(nameSpan);
    item.appendChild(delBtn);
    item.onclick = () => selectProject(p.id);
    list.appendChild(item);
  }
}

async function selectProject(id) {
  state.activeProjectId = id;
  state.activeTaskId = null;
  const p = state.projects.find((x) => x.id === id);
  document.getElementById("active-project-label").textContent = "Project";
  document.getElementById("active-project-name").textContent = p ? p.name : "Untitled";
  renderProjectList();
  renderTaskDetailEmpty();
  await refreshActiveProjectTasks();
}

// ---------- tasks ----------

async function refreshActiveProjectTasks() {
  if (!state.activeProjectId) return;
  try {
    state.tasks = await api(`/api/projects/${state.activeProjectId}/tasks`);
    renderTaskList();
    renderRoster();
  } catch (e) { /* project may have been removed; ignore */ }
}

function renderTaskList() {
  const list = document.getElementById("task-list");
  list.innerHTML = "";
  if (!state.tasks.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "No tasks yet. Assign one above.";
    list.appendChild(empty);
    return;
  }
  for (const t of state.tasks) {
    const card = document.createElement("div");
    card.className = "task-card" + (t.id === state.activeTaskId ? " active" : "");
    card.onclick = () => selectTask(t.id);
    const top = document.createElement("div");
    top.className = "task-card-top";
    const pill = document.createElement("span");
    pill.className = `status-pill status-${t.status}`;
    pill.textContent = t.status;
    const time = document.createElement("span");
    time.className = "hint";
    time.textContent = new Date(t.created_at * 1000).toLocaleString();
    const delBtn = document.createElement("button");
    delBtn.className = "row-delete-btn";
    delBtn.textContent = "×";
    delBtn.title = "Delete this task";
    delBtn.onclick = async (e) => {
      e.stopPropagation();
      if (t.status === "running") { showError("Can't delete a task that's currently running."); return; }
      if (!confirm("Delete this task and its history? This can't be undone.")) return;
      await api(`/api/tasks/${t.id}`, { method: "DELETE" });
      if (state.activeTaskId === t.id) {
        state.activeTaskId = null;
        renderTaskDetailEmpty();
      }
      await refreshActiveProjectTasks();
    };
    top.appendChild(pill);
    top.appendChild(time);
    top.appendChild(delBtn);
    const desc = document.createElement("div");
    desc.className = "task-card-desc";
    desc.textContent = t.description;
    card.appendChild(top);
    card.appendChild(desc);
    list.appendChild(card);
  }
}

function selectTask(id) {
  state.activeTaskId = id;
  state.editingTaskId = null;
  renderTaskList();
  refreshActiveTaskDetail(true);
}

function renderTaskDetailEmpty() {
  document.getElementById("task-detail").innerHTML =
    '<div class="empty-state">Select a task to see live agent activity, files, and status.</div>';
}

async function refreshActiveTaskDetail() {
  if (!state.activeTaskId) return;
  if (state.editingTaskId === state.activeTaskId) return; // don't blow away an in-progress edit
  const panel = document.getElementById("task-detail");
  const focused = document.activeElement;
  if (focused && focused.tagName === "TEXTAREA" && panel.contains(focused) && focused.value.trim()) {
    return; // user is actively typing (e.g. a follow-up) -- don't wipe it out from under them
  }
  const [task, logs, files, attachments] = await Promise.all([
    api(`/api/tasks/${state.activeTaskId}`),
    api(`/api/tasks/${state.activeTaskId}/logs`),
    api(`/api/tasks/${state.activeTaskId}/files`),
    api(`/api/tasks/${state.activeTaskId}/attachments`),
  ]);
  renderTaskDetail(task, logs, files, attachments);
  renderRoster(logs, task.status);

  const prevStatus = state.lastSeenTaskStatus[task.id];
  const justFinished = prevStatus && prevStatus !== task.status && (task.status === "done" || task.status === "failed");
  state.lastSeenTaskStatus[task.id] = task.status;
  if (justFinished && state.conversationMode && task.status === "done" && task.result_summary) {
    readAloud(task.result_summary, null);
  }

  // keep list pill statuses fresh too
  const idx = state.tasks.findIndex((t) => t.id === task.id);
  if (idx >= 0) state.tasks[idx] = task;
  renderTaskList();
}

function renderTaskDetail(task, logs, files, attachments) {
  const el = document.getElementById("task-detail");
  const prevScrollTop = el.scrollTop;
  const wasNearBottom = el.scrollHeight - el.clientHeight - el.scrollTop < 100;
  el.innerHTML = "";

  const desc = document.createElement("div");
  desc.className = "detail-desc";
  const statusPill = `<span class="status-pill status-${task.status}">${task.status}</span>`;
  const followupTag = task.parent_task_id
    ? `<span class="hint" style="margin-left:8px;">↳ follow-up to task #${task.parent_task_id}</span>`
    : "";
  desc.innerHTML = `${statusPill} &nbsp; <span id="desc-text">${escapeHtml(task.description)}</span>${followupTag}`;

  const actions = document.createElement("div");
  actions.className = "detail-actions";

  if (task.status === "done" || task.status === "failed") {
    const retryBtn = document.createElement("button");
    retryBtn.className = "read-aloud-btn";
    retryBtn.textContent = "🔁 Retry (same prompt + attachments)";
    retryBtn.onclick = async () => {
      retryBtn.disabled = true;
      try {
        await api(`/api/tasks/${task.id}/retry`, { method: "POST" });
        await refreshActiveTaskDetail();
        await refreshActiveProjectTasks();
      } catch (e) {
        showError("Could not retry: " + e.message);
      } finally {
        retryBtn.disabled = false;
      }
    };
    actions.appendChild(retryBtn);

    const editBtn = document.createElement("button");
    editBtn.className = "read-aloud-btn";
    editBtn.textContent = "✏️ Edit & retry";
    editBtn.onclick = () => startEditingTask(task);
    actions.appendChild(editBtn);
  }

  const copyAllBtn = document.createElement("button");
  copyAllBtn.className = "read-aloud-btn";
  copyAllBtn.textContent = "📋 Copy full transcript";
  copyAllBtn.onclick = () => copyTranscript(task, logs, copyAllBtn);
  actions.appendChild(copyAllBtn);

  const downloadBtn = document.createElement("button");
  downloadBtn.className = "read-aloud-btn";
  downloadBtn.textContent = "⬇ Download transcript (.txt)";
  downloadBtn.onclick = () => triggerTextDownload(`task_${task.id}_transcript.txt`, buildTranscriptText(task, logs));
  actions.appendChild(downloadBtn);

  el.appendChild(desc);
  el.appendChild(actions);

  if (attachments && attachments.length) {
    const label = document.createElement("div");
    label.className = "detail-section-label";
    label.textContent = "Attached by you";
    el.appendChild(label);
    const wrap = document.createElement("div");
    for (const a of attachments) {
      const chip = document.createElement("span");
      chip.className = "attachment-chip";
      chip.textContent = "📎 " + a.filename;
      wrap.appendChild(chip);
    }
    el.appendChild(wrap);
  }

  if (files.length) {
    const label = document.createElement("div");
    label.className = "detail-section-label";
    label.textContent = "Files produced";
    el.appendChild(label);
    const wrap = document.createElement("div");
    for (const f of files) {
      const chip = document.createElement("button");
      chip.className = "file-chip";
      chip.type = "button";
      chip.textContent = "📄 " + f.filename + " ⬇";
      chip.onclick = () =>
        downloadFromGet(`/api/tasks/${task.id}/files/${f.id}/download`, f.filename);
      wrap.appendChild(chip);
    }
    if (files.length > 1) {
      const allBtn = document.createElement("button");
      allBtn.className = "download-all-link";
      allBtn.type = "button";
      allBtn.textContent = "Download all (.zip)";
      allBtn.onclick = () =>
        downloadFromGet(`/api/tasks/${task.id}/files.zip`, `task_${task.id}_files.zip`);
      wrap.appendChild(allBtn);
    }
    el.appendChild(wrap);
  }

  const label2 = document.createElement("div");
  label2.className = "detail-section-label";
  label2.textContent = "Team activity";
  el.appendChild(label2);

  for (const log of logs) {
    const entry = document.createElement("div");
    entry.className = "log-entry";
    const role = document.createElement("div");
    role.className = "log-role" + (log.role === "system" ? " system" : "");
    role.textContent = roleLabel(log.role);
    const speakBtn = document.createElement("button");
    speakBtn.className = "read-aloud-btn";
    speakBtn.textContent = "🔊 Read aloud";
    speakBtn.onclick = () => readAloud(log.message, speakBtn);
    const copyBtn = document.createElement("button");
    copyBtn.className = "read-aloud-btn";
    copyBtn.textContent = "📋 Copy";
    copyBtn.onclick = () => {
      navigator.clipboard.writeText(log.message);
      copyBtn.textContent = "✓ Copied";
      setTimeout(() => { copyBtn.textContent = "📋 Copy"; }, 1200);
    };
    role.appendChild(speakBtn);
    role.appendChild(copyBtn);
    const msg = document.createElement("div");
    msg.className = "log-msg";
    msg.textContent = log.message;
    entry.appendChild(role);
    entry.appendChild(msg);
    el.appendChild(entry);
  }

  if (task.status === "done") {
    const followup = document.createElement("div");
    followup.className = "followup-box";
    const label = document.createElement("div");
    label.className = "detail-section-label";
    label.textContent = "Continue this conversation";
    followup.appendChild(label);
    const row = document.createElement("div");
    row.className = "followup-row";
    const textarea = document.createElement("textarea");
    textarea.rows = 2;
    textarea.placeholder = "Ask a follow-up or request changes -- the team keeps the context from above...";
    const sendBtn = document.createElement("button");
    sendBtn.className = "primary-btn";
    sendBtn.textContent = "Continue →";
    sendBtn.onclick = async () => {
      const text = textarea.value.trim();
      if (!text) return;
      sendBtn.disabled = true;
      try {
        const { id } = await api(`/api/tasks/${task.id}/followup`, {
          method: "POST",
          body: (() => { const fd = new FormData(); fd.append("description", text); return fd; })(),
        });
        await refreshActiveProjectTasks();
        selectTask(id);
      } catch (e) {
        showError("Could not send follow-up: " + e.message);
      } finally {
        sendBtn.disabled = false;
      }
    };
    row.appendChild(textarea);
    row.appendChild(sendBtn);
    followup.appendChild(row);
    el.appendChild(followup);
  }

  el.scrollTop = wasNearBottom ? el.scrollHeight : prevScrollTop;
}

function buildTranscriptText(task, logs) {
  let out = `Task: ${task.description}\nStatus: ${task.status}\n\n`;
  for (const l of logs) {
    out += `--- ${roleLabel(l.role)} ---\n${l.message}\n\n`;
  }
  return out;
}

function copyTranscript(task, logs, btn) {
  navigator.clipboard.writeText(buildTranscriptText(task, logs));
  btn.textContent = "✓ Copied";
  setTimeout(() => { btn.textContent = "📋 Copy full transcript"; }, 1200);
}

function startEditingTask(task) {
  state.editingTaskId = task.id;
  const el = document.getElementById("task-detail");
  const descTextEl = document.getElementById("desc-text");
  if (!descTextEl) return;
  const textarea = document.createElement("textarea");
  textarea.className = "edit-textarea";
  textarea.rows = 3;
  textarea.value = task.description;
  const row = document.createElement("div");
  row.className = "followup-row";
  const saveBtn = document.createElement("button");
  saveBtn.className = "primary-btn";
  saveBtn.textContent = "Save & retry →";
  saveBtn.onclick = async () => {
    const newText = textarea.value.trim();
    if (!newText) return;
    saveBtn.disabled = true;
    try {
      await api(`/api/tasks/${task.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description: newText }),
      });
      await api(`/api/tasks/${task.id}/retry`, { method: "POST" });
      state.editingTaskId = null;
      await refreshActiveTaskDetail();
      await refreshActiveProjectTasks();
    } catch (e) {
      showError("Could not save: " + e.message);
      state.editingTaskId = null;
    } finally {
      saveBtn.disabled = false;
    }
  };
  const cancelBtn = document.createElement("button");
  cancelBtn.className = "ghost-btn";
  cancelBtn.textContent = "Cancel";
  cancelBtn.onclick = () => {
    state.editingTaskId = null;
    refreshActiveTaskDetail();
  };
  row.appendChild(saveBtn);
  row.appendChild(cancelBtn);
  descTextEl.replaceWith(textarea);
  textarea.insertAdjacentElement("afterend", row);
  textarea.focus();
}

function roleLabel(key) {
  if (state.roles[key]) return state.roles[key].label;
  if (key === "system") return "System";
  return key;
}

function renderSelectedFiles() {
  const wrap = document.getElementById("selected-files");
  wrap.innerHTML = "";
  state.selectedFiles.forEach((file, idx) => {
    const chip = document.createElement("span");
    chip.className = "selected-file-chip";
    chip.textContent = file.name;
    const remove = document.createElement("button");
    remove.textContent = "×";
    remove.onclick = () => {
      state.selectedFiles.splice(idx, 1);
      renderSelectedFiles();
    };
    chip.appendChild(remove);
    wrap.appendChild(chip);
  });
}

async function submitTask() {
  const input = document.getElementById("task-input");
  const text = input.value.trim();
  if (!text) return;
  if (!state.activeProjectId) {
    // Shouldn't normally happen (refreshProjects auto-creates one), but
    // never block the person on project bookkeeping -- just make one.
    const { id } = await api("/api/projects", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: "General" }),
    });
    state.activeProjectId = id;
    await refreshProjects();
  }
  const btn = document.getElementById("submit-task-btn");
  btn.disabled = true;
  try {
    const formData = new FormData();
    formData.append("description", text);
    for (const file of state.selectedFiles) {
      formData.append("files", file);
    }
    const res = await fetch(`/api/projects/${state.activeProjectId}/tasks`, {
      method: "POST",
      body: formData,
    });
    if (!res.ok) {
      const detail = await res.json().catch(() => ({}));
      throw new Error(detail.detail || "Could not create task");
    }
    const { id } = await res.json();
    input.value = "";
    state.selectedFiles = [];
    renderSelectedFiles();
    await refreshActiveProjectTasks();
    selectTask(id);
  } catch (e) {
    showError(e.message);
  } finally {
    btn.disabled = false;
  }
}

// ---------- roster ----------

function renderRoster(logs, taskStatus) {
  const roster = document.getElementById("roster");
  roster.innerHTML = "";
  const countEl = document.getElementById("roster-count");
  if (countEl) countEl.textContent = `(${ROLE_ORDER.length})`;

  let lastActiveRole = null;
  const seenRoles = new Set();
  if (logs) {
    for (const l of logs) {
      if (l.role !== "system") {
        seenRoles.add(l.role);
        lastActiveRole = l.role;
      }
    }
  }

  for (const key of ROLE_ORDER) {
    const role = state.roles[key];
    if (!role) continue;
    const card = document.createElement("div");
    card.className = "roster-card";
    const dot = document.createElement("span");
    dot.className = "roster-dot";
    let stateLabel = "idle";
    if (logs) {
      if (key === lastActiveRole && taskStatus === "running") {
        dot.classList.add("thinking");
        stateLabel = "working";
      } else if (key === lastActiveRole && taskStatus === "failed") {
        dot.classList.add("failed");
        stateLabel = "error";
      } else if (seenRoles.has(key)) {
        dot.classList.add("done");
        stateLabel = "done";
      }
    }
    const name = document.createElement("span");
    name.className = "roster-name";
    name.textContent = role.label;
    const st = document.createElement("span");
    st.className = "roster-state";
    st.textContent = stateLabel;
    card.appendChild(dot);
    card.appendChild(name);
    card.appendChild(st);
    roster.appendChild(card);
  }
}

// ---------- settings ----------

async function openSettings() {
  try {
    state.settings = await api("/api/settings");
    document.getElementById("setting-concurrency").value = state.settings.concurrency || "2";
    document.getElementById("setting-encryption").checked = state.settings.encryption_enabled === "true";
    document.getElementById("setting-lan").checked = state.settings.lan_access_enabled === "true";
    document.getElementById("setting-web-research").checked = state.settings.web_research_enabled === "true";
    await renderLanInfo();

    const container = document.getElementById("role-models");
    container.innerHTML = "";
    const note = document.getElementById("models-note");
    note.textContent = "";

    try {
      const m = await api("/api/models");
      state.availableModels = m.models;
      if (!m.models.length) {
        note.textContent = "No local models found. Pull one with: ollama pull qwen2.5-coder:7b";
      }
    } catch (e) {
      state.availableModels = [];
      note.textContent = "Could not reach Ollama — make sure it's installed and running, then reopen Settings.";
    }

    for (const key of ROLE_ORDER) {
      const role = state.roles[key];
      if (!role) continue;
      const row = document.createElement("div");
      row.className = "role-model-row";
      const label = document.createElement("label");
      label.textContent = role.label;
      const select = document.createElement("select");
      select.id = `model-select-${key}`;
      const current = state.settings[role.settings_key] || "";
      const options = new Set(state.availableModels);
      if (current) options.add(current);
      for (const modelName of options) {
        const opt = document.createElement("option");
        opt.value = modelName;
        opt.textContent = modelName;
        if (modelName === current) opt.selected = true;
        select.appendChild(opt);
      }
      row.appendChild(label);
      row.appendChild(select);
      container.appendChild(row);
    }

    const specialistSelect = document.getElementById("model-select-specialist");
    specialistSelect.innerHTML = "";
    const specialistCurrent = state.settings.model_specialist || "";
    const specialistOptions = new Set(state.availableModels);
    if (specialistCurrent) specialistOptions.add(specialistCurrent);
    for (const modelName of specialistOptions) {
      const opt = document.createElement("option");
      opt.value = modelName;
      opt.textContent = modelName;
      if (modelName === specialistCurrent) opt.selected = true;
      specialistSelect.appendChild(opt);
    }

    document.getElementById("settings-modal").classList.remove("hidden");
  } catch (e) {
    showError("Could not load settings: " + e.message);
  }
}

async function renderLanInfo() {
  const box = document.getElementById("lan-info");
  try {
    const net = await api("/api/network");
    if (net.lan_access_enabled) {
      const url = `http://${net.lan_ip}:${net.port}/?code=${net.access_code}`;
      box.className = "lan-info";
      box.innerHTML =
        `On your phone, connect to the <b>same WiFi</b> as this PC, then open:<br>` +
        `<span class="lan-url">${url}</span><br>` +
        `This PC keeps doing all the work — your phone is just a remote screen for it.`;
    } else {
      box.className = "lan-info off";
      box.textContent = "Off — only this computer can use the workspace.";
    }
  } catch (e) {
    box.className = "lan-info off";
    box.textContent = "Could not load network info.";
  }
}

async function saveSettings() {
  const btn = document.getElementById("save-settings-btn");
  const originalLabel = btn.textContent;
  btn.disabled = true;
  try {
    const values = {
      concurrency: document.getElementById("setting-concurrency").value || "2",
      encryption_enabled: document.getElementById("setting-encryption").checked ? "true" : "false",
      lan_access_enabled: document.getElementById("setting-lan").checked ? "true" : "false",
      web_research_enabled: document.getElementById("setting-web-research").checked ? "true" : "false",
    };
    for (const key of ROLE_ORDER) {
      const role = state.roles[key];
      if (!role) continue;
      const select = document.getElementById(`model-select-${key}`);
      if (select && select.value) values[role.settings_key] = select.value;
    }
    const specialistSelect = document.getElementById("model-select-specialist");
    if (specialistSelect && specialistSelect.value) values.model_specialist = specialistSelect.value;
    state.settings = await api("/api/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ values }),
    });
    await renderLanInfo();
    btn.textContent = "Saved ✓";
    setTimeout(() => { btn.textContent = originalLabel; }, 1500);
  } catch (e) {
    showError("Could not save settings: " + e.message);
  } finally {
    btn.disabled = false;
  }
}

// ---------- new project modal ----------

function openNewProjectModal() {
  document.getElementById("new-project-name").value = "";
  document.getElementById("new-project-modal").classList.remove("hidden");
}

async function createProject() {
  const name = document.getElementById("new-project-name").value.trim();
  if (!name) return;
  try {
    const { id } = await api("/api/projects", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });
    document.getElementById("new-project-modal").classList.add("hidden");
    await refreshProjects();
    selectProject(id);
  } catch (e) {
    showError("Could not create project: " + e.message);
  }
}

// ---------- utils ----------

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function bindEvents() {
  document.getElementById("submit-task-btn").onclick = submitTask;
  document.getElementById("task-input").addEventListener("keydown", (e) => {
    if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) submitTask();
  });
  document.getElementById("attach-files-btn").onclick = () =>
    document.getElementById("task-files").click();
  document.getElementById("task-files").addEventListener("change", (e) => {
    state.selectedFiles.push(...Array.from(e.target.files));
    e.target.value = "";
    renderSelectedFiles();
  });
  document.getElementById("mic-btn").onclick = toggleMic;
  document.getElementById("conversation-btn").onclick = toggleConversationMode;
  document.getElementById("roster-toggle").onclick = () => {
    const roster = document.getElementById("roster");
    const caret = document.getElementById("roster-caret");
    roster.classList.toggle("hidden");
    caret.textContent = roster.classList.contains("hidden") ? "▸" : "▾";
  };
  document.getElementById("settings-btn").onclick = openSettings;
  document.getElementById("close-settings-btn").onclick = () =>
    document.getElementById("settings-modal").classList.add("hidden");
  document.getElementById("save-settings-btn").onclick = saveSettings;

  document.getElementById("new-project-btn").onclick = openNewProjectModal;
  document.getElementById("close-new-project-btn").onclick = () =>
    document.getElementById("new-project-modal").classList.add("hidden");
  document.getElementById("create-project-btn").onclick = createProject;
  bindMediaTools();
}

init();
