from flask import Flask, jsonify, request, send_from_directory
from os_registry import WorkspaceOSEngine
import os

app = Flask(__name__, static_folder='static')

# Initialize the Master OS Engine
os_engine = WorkspaceOSEngine()

# Simulate a System Boot Event when the server starts
os_engine.event_bus.publish('SYSTEM_BOOT', {'os': 'Web/Desktop', 'arch': 'Command Center'})

@app.route('/')
def index():
    if os.path.exists(os.path.join(app.static_folder, 'index.html')):
        return send_from_directory(app.static_folder, 'index.html')
    return '<h1>AI Workspace OS Command Center</h1><p>System is online and running securely.</p>'

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        'status': 'online', 
        'os_state': os_engine.state,
        'message': 'All systems operational.'
    })

@app.route('/api/execute', methods=['POST'])
def execute_task():
    data = request.json
    if not data or 'task_type' not in data:
        return jsonify({'error': 'Missing task_type payload'}), 400
    
    task_type = data['task_type']
    payload = data.get('payload', {})
    user_level = data.get('user_level', 1)
    
    # Route all requests strictly through the central OS Engine
    result = os_engine.execute_central_task(task_type, payload, user_level)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
