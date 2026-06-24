import socket
import io
import json
import zipfile
from fastapi import FastAPI, HTTPException, Request, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response, StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import PlainTextResponse
from pydantic import BaseModel
from pathlib import Path
from typing import List

from . import storage, orchestrator, ollama_client, file_extract, speech, media_tools
from .agents import ROLES

app = FastAPI(title="AI Workspace")
app.state.port = None  # set by main.py after picking a free port

LOCAL_HOSTS = {"127.0.0.1", "::1", "localhost"}


def get_lan_ip() -> str:
    """Best-effort LAN IP of this machine (no packets actually sent)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


class LanAccessMiddleware(BaseHTTPMiddleware):
    """
    Requests from this machine itself (the desktop window) are always
    allowed. Requests from other devices on the network (e.g. a phone)
    are only allowed if LAN access is explicitly turned on in Settings,
    and only with the correct access code -- so simply being on the same
    WiFi isn't enough on its own.
    """

    async def dispatch(self, request: Request, call_next):
        client_host = request.client.host if request.client else ""
        if client_host in LOCAL_HOSTS:
            return await call_next(request)

        settings = storage.get_settings()
        if settings.get("lan_access_enabled") != "true":
            return PlainTextResponse("LAN access is turned off on this AI Workspace.", status_code=403)

        code = request.query_params.get("code") or request.cookies.get("access_code")
        if code != settings.get("access_code"):
            return PlainTextResponse("Missing or incorrect access code.", status_code=403)

        response = await call_next(request)
        if request.query_params.get("code"):
            response.set_cookie("access_code", code, max_age=60 * 60 * 24 * 30)
        return response


app.add_middleware(LanAccessMiddleware)


class NoCacheMiddleware(BaseHTTPMiddleware):
    """Prevents the embedded browser from caching stale HTML/JS/CSS across
    app updates -- without this, a webview can keep running old frontend
    code after files on disk have changed."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        return response


app.add_middleware(NoCacheMiddleware)

# Local-only app; CORS is irrelevant for security here since nothing is
# exposed beyond localhost, but kept permissive for the embedded webview.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup():
    storage.init_db()
    orchestrator.start_scheduler()


# ---------- health / models ----------

@app.get("/api/health")
def health():
    return {"ollama_running": ollama_client.is_running()}


@app.get("/api/voice/status")
def voice_status():
    return {"model_available": speech.is_model_available()}


@app.post("/api/voice/transcribe")
async def voice_transcribe(audio: UploadFile = File(...)):
    raw = await audio.read()
    try:
        text = speech.transcribe_wav_bytes(raw)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not process audio: {e}")
    return {"text": text}


# ---------- media tools (deterministic, local, no AI model) ----------

@app.post("/api/media/split-grid")
async def media_split_grid(
    image: UploadFile = File(...),
    rows: int = Form(...),
    cols: int = Form(...),
):
    raw = await image.read()
    try:
        tiles = media_tools.split_grid(raw, rows, cols)
        zip_bytes = media_tools.tiles_to_zip(tiles)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not split image: {e}")
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="split_images.zip"'},
    )


@app.post("/api/media/edit")
async def media_edit(
    image: UploadFile = File(...),
    operation: str = Form(...),
    params: str = Form("{}"),
):
    raw = await image.read()
    try:
        parsed_params = json.loads(params) if params else {}
        result = media_tools.edit_image(raw, operation, parsed_params)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not edit image: {e}")
    fmt = (parsed_params.get("format") or "png").lower()
    if fmt == "jpg":
        fmt = "jpeg"
    return Response(
        content=result,
        media_type=f"image/{fmt}",
        headers={"Content-Disposition": f'attachment; filename="edited.{fmt}"'},
    )


@app.post("/api/media/logo")
def media_logo(
    text: str = Form(...),
    subtext: str = Form(""),
    palette: str = Form("midnight"),
):
    try:
        png = media_tools.generate_logo(text, subtext, palette)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not generate logo: {e}")
    return Response(
        content=png,
        media_type="image/png",
        headers={"Content-Disposition": 'attachment; filename="logo.png"'},
    )


@app.post("/api/media/slideshow")
async def media_slideshow(
    images: List[UploadFile] = File(...),
    seconds_per_slide: float = Form(2.0),
    output_format: str = Form("gif"),
):
    raw_images = [await f.read() for f in images]
    try:
        if output_format == "mp4":
            data = media_tools.make_slideshow_mp4(raw_images, seconds_per_slide)
            media_type, ext = "video/mp4", "mp4"
        else:
            data = media_tools.make_slideshow_gif(raw_images, seconds_per_slide)
            media_type, ext = "image/gif", "gif"
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not create slideshow: {e}")
    return Response(
        content=data,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="slideshow.{ext}"'},
    )


@app.get("/api/network")
def network():
    settings = storage.get_settings()
    port = app.state.port or "????"
    return {
        "lan_ip": get_lan_ip(),
        "port": port,
        "lan_access_enabled": settings.get("lan_access_enabled") == "true",
        "access_code": settings.get("access_code"),
    }


@app.get("/api/models")
def models():
    try:
        return {"models": ollama_client.list_models()}
    except ollama_client.OllamaError as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/api/roles")
def roles():
    return {k: {"label": v["label"], "settings_key": v["settings_key"]} for k, v in ROLES.items()}


# ---------- settings ----------

@app.get("/api/settings")
def get_settings():
    return storage.get_settings()


class SettingsUpdate(BaseModel):
    values: dict


@app.post("/api/settings")
def post_settings(body: SettingsUpdate):
    storage.set_settings(body.values)
    return storage.get_settings()


# ---------- projects ----------

class ProjectCreate(BaseModel):
    name: str


@app.get("/api/projects")
def get_projects():
    return storage.list_projects()


@app.post("/api/projects")
def post_project(body: ProjectCreate):
    pid = storage.create_project(body.name.strip() or "Untitled project")
    return {"id": pid}


@app.delete("/api/projects/{project_id}")
def delete_project(project_id: int):
    storage.delete_project(project_id)
    return {"ok": True}


# ---------- tasks ----------

@app.get("/api/projects/{project_id}/tasks")
def get_tasks(project_id: int):
    return storage.list_tasks(project_id)


@app.post("/api/projects/{project_id}/tasks")
async def post_task(
    project_id: int,
    description: str = Form(...),
    files: List[UploadFile] = File(default=[]),
):
    if not description.strip():
        raise HTTPException(status_code=400, detail="Task description is required")

    attachments = []
    for f in files:
        if not f.filename:
            continue
        raw = await f.read()
        if file_extract.is_image(f.filename):
            import base64
            attachments.append({
                "filename": f.filename,
                "text": "IMAGE_BASE64::" + base64.b64encode(raw).decode("ascii"),
                "note": None,
            })
        else:
            text, note = file_extract.extract_text(f.filename, raw)
            attachments.append({"filename": f.filename, "text": text, "note": note})

    tid = storage.create_task(project_id, description.strip(), attachments)
    return {"id": tid}


@app.post("/api/tasks/{task_id}/retry")
def retry_task(task_id: int):
    t = storage.get_task(task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    if t["status"] == "running":
        raise HTTPException(status_code=409, detail="Task is already running")
    storage.add_log(task_id, "system", "Retrying task (same description and attachments)...")
    storage.update_task_status(task_id, "queued")
    return {"ok": True}


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    t = storage.get_task(task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    if t["status"] == "running":
        raise HTTPException(status_code=409, detail="Can't delete a task that's currently running")
    storage.delete_task(task_id)
    return {"ok": True}


class TaskEdit(BaseModel):
    description: str


@app.put("/api/tasks/{task_id}")
def edit_task(task_id: int, body: TaskEdit):
    t = storage.get_task(task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    if t["status"] == "running":
        raise HTTPException(status_code=409, detail="Can't edit a task that's currently running")
    if not body.description.strip():
        raise HTTPException(status_code=400, detail="Description can't be empty")
    storage.update_task_description(task_id, body.description.strip())
    return {"ok": True}


@app.post("/api/tasks/{task_id}/followup")
async def followup_task(
    task_id: int,
    description: str = Form(...),
    files: List[UploadFile] = File(default=[]),
):
    parent = storage.get_task(task_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent task not found")
    if not description.strip():
        raise HTTPException(status_code=400, detail="Description is required")

    attachments = []
    for f in files:
        if not f.filename:
            continue
        raw = await f.read()
        if file_extract.is_image(f.filename):
            import base64
            attachments.append({
                "filename": f.filename,
                "text": "IMAGE_BASE64::" + base64.b64encode(raw).decode("ascii"),
                "note": None,
            })
        else:
            text, note = file_extract.extract_text(f.filename, raw)
            attachments.append({"filename": f.filename, "text": text, "note": note})

    new_id = storage.create_task(
        parent["project_id"], description.strip(), attachments, parent_task_id=task_id
    )
    return {"id": new_id}


@app.get("/api/tasks/{task_id}")
def get_task(task_id: int):
    t = storage.get_task(task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    return t


@app.get("/api/tasks/{task_id}/logs")
def get_logs(task_id: int):
    return storage.get_logs(task_id)


@app.get("/api/tasks/{task_id}/attachments")
def get_attachments(task_id: int):
    return storage.get_attachments(task_id)


@app.get("/api/tasks/{task_id}/files")
def get_files(task_id: int):
    files = storage.get_files(task_id)
    return [
        {
            "id": f["id"],
            "filename": f["filename"],
            "created_at": f["created_at"],
            "is_binary": f.get("is_binary", False),
            "size": len(f["content"]) if f["content"] is not None else 0,
        }
        for f in files
    ]


MIME_TYPES = {
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}


@app.get("/api/tasks/{task_id}/files/{file_id}/download")
def download_file(task_id: int, file_id: int):
    files = storage.get_files(task_id)
    f = next((x for x in files if x["id"] == file_id), None)
    if not f:
        raise HTTPException(status_code=404, detail="File not found")
    safe_name = f["filename"].split("/")[-1].split("\\")[-1]
    ext = safe_name.rsplit(".", 1)[-1].lower() if "." in safe_name else ""
    media_type = MIME_TYPES.get(ext, "application/octet-stream")
    return Response(
        content=f["content"],
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{safe_name}"'},
    )


@app.get("/api/tasks/{task_id}/files.zip")
def download_all_files(task_id: int):
    files = storage.get_files(task_id)
    if not files:
        raise HTTPException(status_code=404, detail="No files for this task")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.writestr(f["filename"], f["content"])
    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="task_{task_id}_files.zip"'},
    )


# Serve the frontend last so /api/* routes above take priority.
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
