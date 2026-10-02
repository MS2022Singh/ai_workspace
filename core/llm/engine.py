import litellm
from core.prompts.mode_manager import get_system_prompt

async def generate_response(user_input: str, mode: str = "auto", context: str = ""):
    system_prompt = get_system_prompt(mode)
    if context and context.strip():
        system_prompt += f"\n\n=== VERIFIED CONTEXT (use only this for citations) ===\n{context}\n=== END VERIFIED CONTEXT ==="
    else:
        system_prompt += "\n\n[NO VERIFIED CONTEXT PROVIDED — Do not cite any source. If the user asks for citations, respond: 'I couldn't verify this from an authoritative source.']"
    
    try:
        response = await litellm.acompletion(
            model="ollama/llama3",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            timeout=120
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[LLM OFFLINE] {str(e)}. Ensure 'ollama serve' is running."
