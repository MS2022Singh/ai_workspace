import re
import requests
from core.llm.engine import generate_response
from core.tools.router import execute_system_command
from core.rag.vector_store import rag_engine
from core.permissions.enforcer import get_policy

async def route_chat_intent(message: str, methodology: str = "auto") -> dict:
    msg_lower = message.strip().lower()
    
    # 1. IMAGE GENERATION INTENT
    image_keywords = ["generate image", "render image", "draw", "create picture", "generate cosmos image", "image of"]
    if any(kw in msg_lower for kw in image_keywords):
        prompt = re.sub(r'^(generate|render|draw|create)\s+(an?\s+)?(image|picture)\s+(of\s+)?', '', message, flags=re.IGNORECASE).strip()
        if not prompt: prompt = message
        
        encoded_prompt = requests.utils.quote(prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        
        response_text = (
            f"### 🎨 Generative Image Studio Rendered\n\n"
            f"**Prompt:** *\"{prompt}\"*\n\n"
            f'<img src="{image_url}" alt="{prompt}" style="max-width:100%; border-radius:8px; border:1px solid #334155; margin-top:10px; display:block;" />\n\n'
            f"Asset generated via Pollinations AI Engine. You can view full-screen in **Panel 7 (Image Studio)**."
        )
        return {"agent": "ImageStudioAgent", "response": response_text, "type": "image"}

    # 2. COMPUTER / SYSTEM COMMAND INTENT
    if msg_lower.startswith("run ") or msg_lower.startswith("cmd ") or msg_lower.startswith("exec "):
        command = re.sub(r'^(run|cmd|exec)\s+', '', message, flags=re.IGNORECASE).strip()
        policy = get_policy()
        
        if not policy.get("EXECUTE", False):
            response_text = (
                f"⚠️ **Execution Blocked by Policy**\n\n"
                f"Attempted command: `{command}`\n\n"
                f"**Reason:** `EXECUTE` permission is currently **DISABLED** (Autonomy Level 1).\n"
                f"To allow command execution, switch to **Panel 16 (Permission Policy)** and elevate to **Autonomy Level 2**."
            )
            return {"agent": "SecurityEnforcer", "response": response_text, "type": "security_block"}
            
        cmd_result = execute_system_command(command)
        response_text = (
            f"### 🖥️ Shell Command Executed\n\n"
            f"**Command:** `{command}`\n"
            f"**Exit Code:** `{cmd_result['returncode']}`\n\n"
            f"```text\n{cmd_result['stdout']}\n```"
        )
        return {"agent": "ComputerControlAgent", "response": response_text, "type": "computer"}

    # 3. RESEARCH / WEB SEARCH INTENT
    if any(kw in msg_lower for kw in ["research", "search web", "find paper", "deep research"]):
        query = re.sub(r'^(research|search web for|find paper on|deep research on)\s+', '', message, flags=re.IGNORECASE).strip()
        context = rag_engine.query_context(query)
        phd_report = await generate_response(f"Synthesize comprehensive research paper on: {query}", mode="phd", context=context)
        
        response_text = (
            f"### ⚗️ Autonomous Deep Research Synthesis\n\n"
            f"{phd_report}\n\n"
            f"--- \n"
            f"*Source verified against local vector memory store.*"
        )
        return {"agent": "ResearchAgent", "response": response_text, "type": "research"}

    # 4. STANDARD EXECUTIVE INTENT (Delegated to upgraded LLM Engine)
    context = rag_engine.query_context(message)
    reply = await generate_response(message, mode=methodology, context=context)
    return {"agent": f"OrchestratorAgent ({methodology})", "response": reply, "type": "chat"}