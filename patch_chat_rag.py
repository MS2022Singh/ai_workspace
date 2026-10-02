import re
from pathlib import Path

main_path = Path("main.py")
src = main_path.read_text(encoding="utf-8")

# Match chat_endpoint from decorator through its return statement
pattern = re.compile(
    r'(@app\.post\("/api/chat"\)\s*\nasync def chat_endpoint\(.*?\):\s*\n)(.*?)(?=\n@app\.post)',
    re.DOTALL
)

def patcher(match):
    header = match.group(1)
    tail = match.group(3) if match.lastindex >= 3 else ""
    new_body = (
        '    text = message or "Analyze uploaded file asset."\n'
        '    if file:\n'
        '        text = f"Analyze attached file \'{file.filename}\': {text}"\n'
        '\n'
        '    # RAG: retrieve verified context from ChromaDB\n'
        '    rag_context = ""\n'
        '    try:\n'
        '        from core.rag.vector_store import rag_engine\n'
        '        rag_context = rag_engine.query_context(text, n_results=4)\n'
        '    except Exception as e:\n'
        '        print(f"[RAG WARN] {e}")\n'
        '\n'
        '    actual_response = await generate_response(user_input=text, mode=mode, context=rag_context)\n'
        '    return {\n'
        '        "response": actual_response,\n'
        '        "result": actual_response,\n'
        '        "mode_used": mode,\n'
        '        "rag_context_used": bool(rag_context),\n'
        '        "context_chars": len(rag_context)\n'
        '    }\n'
    )
    return header + new_body + "\n"

new_src, count = pattern.subn(patcher, src)
if count > 0:
    main_path.write_text(new_src, encoding="utf-8")
    print(f"PATCHED: {count} chat endpoint with RAG context injection")
elif "rag_engine.query_context" in src:
    print("SKIP: chat endpoint already has RAG")
else:
    print("ERROR: regex did not match chat_endpoint")
