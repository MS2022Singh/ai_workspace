import logging
from typing import Dict

logger = logging.getLogger("PromptEngine")

class PromptEngine:
    def __init__(self):
        # Maps directly to UI dropdown selections
        self.methodologies: Dict[str, str] = {
            "Standard": "Execute the task precisely and concisely. Prioritize execution over explanation.",
            "Understand Like a Genius": "Explain using first principles, abstract analogies, and deep structural insights before executing.",
            "Master Any Skill": "Break down the requirement into core skill components, provide execution drills, and identify common pitfalls.",
            "Fix Mental Blocks": "Identify cognitive distortions or logical flaws in the request, reframe the approach, and provide a micro-action step.",
            "PhD Breakdown": "Analyze with academic rigor, cite underlying architectural methodologies, and evaluate all edge cases."
        }

    def format_payload(self, raw_task: str, methodology_key: str) -> str:
        system_instruction = self.methodologies.get(methodology_key, self.methodologies["Standard"])
        logger.info(f"Applying prompt methodology: {methodology_key}")
        
        return f"""
        [SYSTEM DIRECTIVE: {methodology_key.upper()}]
        {system_instruction}
        
        [USER TASK]
        {raw_task}
        """

prompt_engine = PromptEngine()
