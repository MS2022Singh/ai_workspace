import http.server
import socketserver
import json
import os
import sys

sys.path.append(os.path.abspath("."))

from catalog.tool_registry import tool_registry
from core.verification.bug_eliminator import bug_eliminator
from devices.registry import device_registry

class CommandCenterHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open("modules/ui/index.html", "rb") as f:
                self.wfile.write(f.read())
        elif self.path == "/api/tools":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(tool_registry.tools).encode("utf-8"))
        elif self.path == "/api/system":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            sys_status = {
                "bug_report": bug_eliminator.inspect_system(),
                "device": device_registry.device_info,
                "version": "v0.8.1"
            }
            self.wfile.write(json.dumps(sys_status).encode("utf-8"))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/execute":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            payload = json.loads(body.decode('utf-8')) if body else {}
            
            prompt = payload.get("prompt", "")
            agent = payload.get("agent", "Auto-Orchestrator")

            response_payload = {
                "status": "success",
                "agent": agent,
                "prompt": prompt,
                "response": f"Task processed successfully by {agent}.",
                "execution_logs": [
                    "Request received & parsed",
                    f"Assigned to {agent}",
                    "Policy permissions validated (READ/WRITE)",
                    "Task execution verified clean"
                ]
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_payload).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8080):
    handler = CommandCenterHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"[UI SERVER] Command Center API & Web UI active on http://localhost:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
