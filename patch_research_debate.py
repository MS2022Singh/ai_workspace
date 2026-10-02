from pathlib import Path

main_path = Path("main.py")
src = main_path.read_text(encoding="utf-8")

# Patch debate endpoint
old_debate = """    response = await generate_response(
        user_input=f"Deconstructed First-Principles Analysis & Multi-Agent Debate for: {text}",
        mode="phd"
    )"""
new_debate = """    from core.rag.vector_store import rag_engine
    ctx = rag_engine.query_context(text, n_results=3)
    response = await generate_response(
        user_input=f"Deconstructed First-Principles Analysis & Multi-Agent Debate for: {text}",
        mode="phd",
        context=ctx
    )"""

# Patch research endpoint
old_research = """    response = await generate_response(
        user_input=f"Synthesize comprehensive academic research paper on: {text}",
        mode="phd"
    )"""
new_research = """    from core.rag.vector_store import rag_engine
    ctx = rag_engine.query_context(text, n_results=5)
    response = await generate_response(
        user_input=f"Synthesize comprehensive academic research paper on: {text}. Include verified sources, contradictions, and confidence levels.",
        mode="phd",
        context=ctx
    )"""

count = 0
if old_debate in src and "ctx = rag_engine.query_context" not in src.split("debate_endpoint")[1][:500]:
    src = src.replace(old_debate, new_debate)
    count += 1
if old_research in src:
    src = src.replace(old_research, new_research)
    count += 1

main_path.write_text(src, encoding="utf-8")
print(f"PATCHED: {count} endpoint(s) with RAG injection")
