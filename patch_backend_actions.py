from pathlib import Path

main_path = Path("main.py")
src = main_path.read_text(encoding="utf-8")

if "api/output/save" in src:
    print("SKIP: output endpoints already exist")
else:
    addition = """

# ============================================================
# 11. OUTPUT MANAGEMENT (Save/Download/List/Delete)
# ============================================================
from pathlib import Path as _Path
import time as _time
import base64 as _b64
import re as _re

OUTPUT_DIR = _Path("storage_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

@app.post("/api/output/save")
async def save_output(payload: dict):
    content = payload.get("content", "")
    name = payload.get("name") or f"output_{int(_time.time())}"
    name = _re.sub(r'[^a-zA-Z0-9_.-]', '_', name)

    if content.startswith("data:") and ";base64," in content:
        header, b64 = content.split(";base64,", 1)
        ext = header.split("/")[1].split(";")[0]
        if not name.endswith(f".{ext}"):
            name = f"{name}.{ext}"
        data = _b64.b64decode(b64)
        out_path = OUTPUT_DIR / name
        out_path.write_bytes(data)
    else:
        if not name.endswith(".txt"):
            name = f"{name}.txt"
        out_path = OUTPUT_DIR / name
        out_path.write_text(content, encoding="utf-8")

    return {
        "status": "saved",
        "filename": name,
        "size": out_path.stat().st_size,
        "download_url": f"/api/output/download/{name}",
        "response": f"Saved as {name}"
    }

@app.get("/api/output/download/{filename}")
async def download_output(filename: str):
    from fastapi.responses import FileResponse
    safe = _Path(filename).name
    path = OUTPUT_DIR / safe
    if not path.exists():
        return {"error": "not_found"}
    return FileResponse(str(path), filename=safe)

@app.get("/api/output/list")
async def list_outputs():
    files = []
    for f in OUTPUT_DIR.iterdir():
        if f.is_file():
            files.append({"name": f.name, "size": f.stat().st_size, "modified": f.stat().st_mtime})
    files.sort(key=lambda x: x["modified"], reverse=True)
    return {"files": files, "count": len(files)}

@app.post("/api/output/delete")
async def delete_output(payload: dict):
    filename = _Path(payload.get("filename", "")).name
    path = OUTPUT_DIR / filename
    if path.exists():
        path.unlink()
        return {"status": "deleted", "filename": filename}
    return {"status": "not_found"}

# ============================================================
# 12. TOOL HUB — Add/Remove Tools
# ============================================================
import json as _json
import subprocess as _sp

TOOLS_DIR = _Path("ai_workspace/tools")
TOOLS_DIR.mkdir(parents=True, exist_ok=True)
TOOLS_CATALOG = _Path("catalog/registry/tools.json")
TOOLS_CATALOG.parent.mkdir(parents=True, exist_ok=True)

@app.post("/api/tools/add")
async def add_tool(payload: dict):
    url = (payload.get("url") or "").strip()
    if not url:
        return {"status": "error", "detail": "URL required"}

    catalog = _json.loads(TOOLS_CATALOG.read_text()) if TOOLS_CATALOG.exists() else {}
    name = url.rstrip("/").split("/")[-1].replace(".git", "")
    if not name:
        name = f"tool_{int(_time.time())}"

    if name in catalog:
        return {"status": "duplicate", "detail": f"{name} already registered", "tool": catalog[name]}

    entry = {"name": name, "url": url, "added": _time.time(), "status": "registered", "path": None}
    try:
        target = TOOLS_DIR / name
        if not target.exists():
            r = _sp.run(["git", "clone", "--depth", "1", url, str(target)],
                        capture_output=True, text=True, timeout=90)
            if r.returncode == 0:
                entry["path"] = str(target)
                entry["status"] = "cloned"
            else:
                entry["clone_error"] = r.stderr[:200]
    except Exception as e:
        entry["clone_error"] = str(e)[:200]

    catalog[name] = entry
    TOOLS_CATALOG.write_text(_json.dumps(catalog, indent=2), encoding="utf-8")
    return {"status": "ok", "tool": entry, "total_tools": len(catalog)}

@app.post("/api/tools/remove")
async def remove_tool(payload: dict):
    name = (payload.get("name") or "").strip()
    if not name or not TOOLS_CATALOG.exists():
        return {"status": "error"}
    catalog = _json.loads(TOOLS_CATALOG.read_text())
    if name not in catalog:
        return {"status": "not_found"}
    removed = catalog.pop(name)
    TOOLS_CATALOG.write_text(_json.dumps(catalog, indent=2), encoding="utf-8")
    if payload.get("delete_files") and removed.get("path"):
        import shutil as _sh
        try:
            _sh.rmtree(removed["path"], ignore_errors=True)
        except Exception:
            pass
    return {"status": "removed", "tool": name, "remaining": len(catalog)}

@app.get("/api/tools/list")
async def list_tools():
    if not TOOLS_CATALOG.exists():
        return {"tools": [], "count": 0}
    catalog = _json.loads(TOOLS_CATALOG.read_text())
    return {"tools": list(catalog.values()), "count": len(catalog)}
"""
    src = src.rstrip() + addition
    main_path.write_text(src, encoding="utf-8")
    print("PATCHED: Added output management + tool add/remove endpoints")
