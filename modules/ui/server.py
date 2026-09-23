import http.server
import socketserver
import json
import sys
import os
sys.path.append(os.path.abspath("."))

from modules.agents.agent_manager import agent_manager
from modules.tools.tool_handler import tool_handler
from catalog.tool_registry import tool_registry

PORT = 8080
UI_DIR = os.path.dirname(__file__)

class WorkspaceRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            payload = json.loads(post_data.decode('utf-8'))
        except Exception:
            self._send_json({"error": "Invalid JSON"}, 400)
            return

        endpoint = self.path
        if endpoint == "/api/dispatch":
            agent_type = payload.get("agent", "research")
            task = payload.get("task", "")
            result = agent_manager.dispatch(agent_type, task)
            self._send_json(result)
        elif endpoint == "/api/tool":
            tool_id = payload.get("tool_id", "")
            params = payload.get("params", {})
            result = tool_handler.execute_tool(tool_id, params)
            self._send_json(result)
        elif endpoint == "/api/tools/toggle":
            tool_id = payload.get("tool_id", "")
            active = payload.get("active", True)
            tool_registry.set_tool_status(tool_id, active)
            self._send_json({"status": "updated", "tools": tool_registry.tools})
        else:
            self._send_json({"error": "Endpoint not found"}, 404)

    def do_GET(self):
        if self.path == "/api/status":
            self._send_json({
                "status": "running",
                "tools": tool_registry.tools,
                "models": tool_registry.models
            })
        elif self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            index_path = os.path.join(UI_DIR, "index.html")
            if os.path.exists(index_path):
                with open(index_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"<h1>AI Workspace Server Running</h1>")
        else:
            super().do_GET()

    def _send_json(self, data, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

def run_server():
    with socketserver.TCPServer(("", PORT), WorkspaceRequestHandler) as httpd:
        print(f"[UI SERVER] Command Center API & Web UI active on http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
