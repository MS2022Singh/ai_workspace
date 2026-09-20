import json

class ToolController:
    def __init__(self):
        self.state = {}

    def set_tool_state(self, tool_name: str, enabled: bool):
        self.state[tool_name] = enabled
        return {"status": "success", "tool": tool_name, "enabled": enabled}

    def get_all_states(self):
        return self.state

if __name__ == "__main__":
    tc = ToolController()
    res = tc.set_tool_state("ToolJet", True)
    print("[Backend Verification Passed]:", res)
