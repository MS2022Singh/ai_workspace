import json
import os

PROMPTS_FILE = os.path.join(os.path.dirname(__file__), "prompts.json")

def get_system_prompt(mode: str) -> str:
    default_prompt = "You are Gem OS, a production-grade AI workspace orchestrator."
    try:
        if os.path.exists(PROMPTS_FILE):
            with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
                prompts = json.load(f)
            return prompts.get(mode.lower(), default_prompt)
    except Exception as e:
        print(f"Error loading prompts: {e}")
    
    hardcoded_prompts = {
        "auto": "You are Gem OS. Analyze the request and respond optimally based on logic and evidence.",
        "phd": "You are a PhD-level Research Agent. Provide deep, cited, and rigorously structured analysis.",
        "attorney": "You are a Legal Agent. Structure responses as formal legal drafts or patent reviews.",
        "skill master": "You are a Skill Master. Break down complex topics into easy, step-by-step learning modules."
    }
    return hardcoded_prompts.get(mode.lower(), default_prompt)
