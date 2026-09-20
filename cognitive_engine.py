class CognitiveEngine:
    PROMPTS = {
        "genius": "UNDERSTAND LIKE A GENIUS: Break down {topic} using advanced analogies, real-world applications, counterexamples, and multi-perspective testing.",
        "master": "MASTER SKILL (20+ YRS): Reverse engineer {topic} and construct a day-by-day roadmap using free/low-cost resources.",
        "blocks": "FIX MENTAL BLOCKS: Analyze {topic} as a cognitive scientist. Identify root causes, behavioral patterns, and design a habit loop to eliminate it.",
        "clarity": "TURN CONFUSION INTO CLARITY: Break down {topic} step-by-step using metaphors, visual imagery, and a memorable mental shortcut framework.",
        "phd": "PhD LEVEL BREAKDOWN: Teach {topic} from first principles, foundational theories, historical evolution, and key literature.",
        "framework": "BUILD MENTAL FRAMEWORK: Create a custom decision framework to evaluate, approach, and master {topic} like a professional.",
        "upgrade": "UPGRADE YOUR BRAIN IN 30 DAYS: Design a 30-day program including high-IQ thinking routines, mind-expanding prompts, memory techniques, and rest habits for {topic}."
    }

    @classmethod
    def generate_prompt(cls, key: str, topic: str) -> str:
        template = cls.PROMPTS.get(key, "Analyze {topic} thoroughly.")
        t = topic.strip() if topic.strip() else "the target domain"
        return template.format(topic=t)
