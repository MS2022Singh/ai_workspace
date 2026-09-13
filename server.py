from flask import Flask, jsonify, request, send_from_directory
import os
from os_registry import WorkspaceOSEngine

app = Flask(__name__, static_folder='static')
os_engine = WorkspaceOSEngine()

# Trigger boot sequence on startup
os_engine.event_bus.publish('SYSTEM_BOOT', {'environment': 'production', 'target': 'multi-platform'})

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "online",
        "os_state": os_engine.state,
        "active_modules": os_engine.upgrader.installed_tools,
        "message": "AI Workspace OS Kernel is running with active UI repositories."
    })

@app.route('/api/modules/toggle', methods=['POST'])
def toggle_module():
    data = request.json or {}
    tool_name = data.get('tool_name')
    active = data.get('active', True)
    result = os_engine.upgrader.set_tool_state(tool_name, active)
    return jsonify(result)

@app.route('/api/execute', methods=['POST'])
def execute_task():
    data = request.json or {}
    task_type = data.get('task_type')
    payload = data.get('payload', {})
    user_level = data.get('user_level', 1)
    
    result = os_engine.execute_central_task(task_type, payload, user_level)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
