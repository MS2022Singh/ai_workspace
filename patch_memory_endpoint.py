from pathlib import Path

main_path = Path("main.py")
src = main_path.read_text(encoding="utf-8")

# --- STEP 1: Remove /api/memory from the stacked decorator ---
stacked = '@app.post("/api/memory")\n@app.post("/api/audio")'
unstacked = '@app.post("/api/audio")'

if stacked in src:
    src = src.replace(stacked, unstacked)
    print("[1/2] Removed /api/memory from stacked decorator")
else:
    print("[1/2] No change - /api/memory was not stacked (or already fixed)")

# --- STEP 2: Insert a real /api/memory endpoint BEFORE the generic one ---
marker = '@app.post("/api/audio")\nasync def generic_panel_handler(payload: UniversalPayload):'

new_endpoint = r'''@app.post("/api/memory")
async def memory_ingest_endpoint(payload: UniversalPayload):
    import requests
    from bs4 import BeautifulSoup
    from core.rag.vector_store import rag_engine
    import hashlib

    text = payload.get_text()

    if not text.startswith("http"):
        return {
            "status": "not_a_url",
            "detail": "Provide a URL starting with http:// or https://",
            "response": "Please provide a URL.",
            "result": "not_a_url",
        }

    try:
        r = requests.get(text, timeout=20, headers={"User-Agent": "Mozilla/5.0 AI-Workspace/5.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        body = " ".join(soup.get_text().split())

        if len(body) < 200:
            return {
                "status": "too_short",
                "chars": len(body),
                "response": "Page too short to index.",
                "result": "short",
            }

        chunks = []
        i = 0
        while i < len(body):
            chunks.append(body[i:i+800])
            i += 700

        stored = 0
        for idx, chunk in enumerate(chunks):
            doc_id = hashlib.md5((text + "#" + str(idx)).encode()).hexdigest()
            try:
                rag_engine.add_document(doc_id=doc_id, text=chunk, source=text)
                stored += 1
            except Exception as inner:
                err = str(inner).lower()
                if ("already" in err) or ("duplicate" in err) or ("unique" in err):
                    pass
                else:
                    raise

        total = rag_engine.collection.count()
        return {
            "status": "indexed",
            "source": text,
            "chunks_stored": stored,
            "chunks_total": len(chunks),
            "chars_extracted": len(body),
            "total_chunks_in_db": total,
            "response": "Indexed " + str(stored) + " new chunks from " + text + ". Vector memory now holds " + str(total) + " chunks total.",
            "result": "Ingestion complete",
        }
    except Exception as e:
        return {
            "status": "error",
            "detail": str(e),
            "response": "Ingestion failed: " + str(e),
            "result": "error",
        }


'''

if marker in src:
    src = src.replace(marker, new_endpoint + marker, 1)
    print("[2/2] Inserted real /api/memory endpoint")
else:
    print("[2/2] WARNING: marker not found - inspect main.py around line 165")

main_path.write_text(src, encoding="utf-8")
print("DONE: main.py patched successfully")
