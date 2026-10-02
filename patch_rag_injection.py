import re
from pathlib import Path

main_path = Path("main.py")
src = main_path.read_text(encoding="utf-8")

old_block = """@app.post("/api/chat")
async def chat_endpoint(
    message: Optional[str] = Form(None),
    mode: Optional[str] = Form("auto"),
    file: Optional[UploadFile] = File(None)
):
    text = message or "Analyze uploaded file asset."
    if file:
        text = f"Analyze attached file '{file.filename}': {text}"

    actual_response = await generate_response(user_input=text, mode=mode)
    return {"response": actual_response, "result": actual_response}"""

new_block = """@app.post("/api/chat")
async def chat_endpoint(
    message: Optional[str] = Form(None),
    mode: Optional[str] = Form("auto"),
    file: Optional[UploadFile] = File(None)
):
    text = message or "Analyze uploaded file asset."
    if file:
        text = f"Analyze attached file '{file.filename}': {text}"

    # NEW: retrieve verified context from RAG (ChromaDB)
    try:
        from core.rag.vector_store import rag_engine
        context = rag_engine.query_context(text, n_results=3)
    except Exception as e:
        context = ""
        print(f"[RAG WARN] {e}")

    actual_response = await generate_response(user_input=text, mode=mode, context=context)
    return {
        "response": actual_response,
        "result": actual_response,
        "mode_used": mode,
        "rag_context_used": bool(context)
    }"""

if old_block in src:
    src = src.replace(old_block, new_block)
    main_path.write_text(src, encoding="utf-8")
    print("PATCHED: RAG context now injected into /api/chat")
elif "rag_engine.query_context" in src:
    print("SKIP: /api/chat already patched")
else:
    print("ERROR: Could not find the exact chat_endpoint block. Manually verify main.py lines 47-58.")
