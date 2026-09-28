class PromptMethodologyEngine:
    TEMPLATES = {
        "genius": "I want to understand {topic} as if I were a genius. Break down concept using advanced analogies, real world applications, counterexamples and multiple perspectives, then test my understanding with expert-level questions.",
        "skill_mastery": "Assume you are a master of {topic} with 20+ years of experience. Reverse engineer the process that got you there and build me a day-by-day plan to reach that level as fast as humanly possible using only free or low-cost resources.",
        "fix_mental_blocks": "I have been struggling with {topic}. Analyze it like a cognitive scientist. Identify the root causes, the behavioural patterns behind it, and design a habit loop to eliminate it.",
        "clarity": "I do not understand {topic}. Break it down step-by-step using metaphors, visual imagery, and real world examples. Then create a mental shortcut or framework I can use to remember it forever.",
        "phd_breakdown": "Teach me {topic} like I am preparing for a PhD. Start from first principles, explain all foundational theories, include historical evolution, and give me key papers/books to go further.",
        "mental_framework": "I am trying to master {topic}. Build me a custom mental model or decision framework that simplifies how to approach, evaluate, and improve in it over time like a pro would.",
        "brain_upgrade_30days": "Design a 30-day brain upgrade program for {topic} that includes high IQ thinking routines, mind-expanding prompts, advanced reading material, memory-enhancing techniques and strategic rest habits."
    }

    @classmethod
    def apply_prompt(cls, key: str, topic: str) -> str:
        template = cls.TEMPLATES.get(key, "Explain {topic} in detail.")
        return template.format(topic=topic)

prompt_engine = PromptMethodologyEngine()
