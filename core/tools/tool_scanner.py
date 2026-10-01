import os, json, subprocess, shlex

TOOLS_DIR = r"C:\AI_Workspace\ai_workspace_core\ai_workspace\tools"

def scan_tools():
    registry = {}
    if not os.path.exists(TOOLS_DIR):
        return registry
    for root, dirs, files in os.walk(TOOLS_DIR):
        for file in files:
            if file in ["main.py", "cli.py", "app.py"]:
                tool_name = os.path.basename(root)
                registry[tool_name] = {"entry": os.path.join(root, file), "dir": root}
    return registry

def execute_tool(entry_path, args_str=""):
    cmd = f'python "{entry_path}" {args_str}'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode}
