class AgentDispatcher:
    def dispatch(self, domain: str, title: str):
        return {"domain": domain, "title": title, "agent": f"{domain.capitalize()}Agent", "status": "assigned"}
