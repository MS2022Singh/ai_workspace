class CognitiveEngine:
    PROMPTS = {
        "genius": "UNDERSTAND LIKE A GENIUS: Break down {topic} using advanced analogies, real-world applications, counterexamples, and multi-perspective testing.",
        "master": "MASTER SKILL (20+ YRS): Reverse engineer {topic} and construct a day-by-day roadmap using free resources.",
        "blocks": "FIX MENTAL BLOCKS: Analyze {topic} as a cognitive scientist. Identify root causes, behavioral patterns, and design a habit loop to eliminate it.",
        "clarity": "CONFUSION TO CLARITY: Break down {topic} step-by-step using metaphors, visual imagery, and a memorable mental shortcut framework.",
        "phd": "PhD LEVEL BREAKDOWN: Teach {topic} from first principles, foundational theories, historical evolution, and key literature.",
        "framework": "BUILD MENTAL FRAMEWORK: Create a custom decision framework to evaluate, approach, and master {topic} like a professional."
    }

    @classmethod
    def generate_prompt(cls, key: str, input_text: str) -> str:
        template = cls.PROMPTS.get(key, "Analyze {topic} thoroughly.")
        topic = input_text.strip() if input_text else "the target domain"
        return template.format(topic=topic)
