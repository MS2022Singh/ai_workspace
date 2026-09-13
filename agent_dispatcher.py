class AgentDispatcher:
    def __init__(self):
        self.experts = {
            'frontend': 'Frontend Developer Expert',
            'backend': 'Backend Systems Expert',
            'qa': 'QA & Testing Specialist',
            'pm': 'Project Manager Expert'
        }

    def dispatch(self, domain: str, task_description: str):
        expert = self.experts.get(domain.lower(), 'General AI Assistant')
        return {
            'domain': domain,
            'assigned_expert': expert,
            'status': 'DISPATCHED',
            'task': task_description
        }
