class MasterToolRegistry:
    CATEGORIES = {
        "Orchestration & Command Center": ["ToolJet", "n8n", "AppFlowy", "Coolify", "Dokploy", "Open WebUI", "Dify"],
        "Multi-Agent & DAG Engines": ["gstack", "Browser Use", "Langflow", "Agno", "OpenHands", "SWE-agent", "Composio"],
        "AI Models & Inference": ["Qwen 3.8", "Unsloth", "Axolotl", "Whisper", "Kokoro TTS", "Ollama Local", "vLLM"],
        "Security, Pentest & OSINT": ["PyRIT", "FreeBuf", "Vulture OSINT", "FinalRecon", "Sherlock", "Maigret", "SpiderFoot"],
        "RAG & Storage": ["Semantica", "AIVM Brain", "Crawl4AI", "Supabase", "yt-dlp"]
    }

    def __init__(self):
        self.tool_states = {t: True for cat in self.CATEGORIES.values() for t in cat}

    def get_all(self):
        return {"categories": self.CATEGORIES, "states": self.tool_states}
