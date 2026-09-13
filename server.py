from flask import Flask, jsonify, request, send_from_directory
from app import CoreApplication
from permissions import PermissionEngine

app = Flask(__name__, static_folder='static')
core_app = CoreApplication(db_path='workspace_memory.db')
permission_engine = PermissionEngine()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({'status': 'operational', 'engine': 'AI Workspace Core OS'})

@app.route('/api/workflow', methods=['POST'])
def run_workflow():
    data = request.json or {}
    task_id = data.get('task_id', 'task_default')
    title = data.get('title', 'Automated Task')
    domain = data.get('domain', 'frontend')
    action = data.get('action_type', 'READ')
    
    perm = permission_engine.check_permission(action, user_authorized_level=1)
    if not perm['allowed'] and perm.get('requires_approval'):
        return jsonify({'status': 'blocked', 'permission': perm}), 403

    result = core_app.run_workflow(task_id, title, domain)
    return jsonify({'status': 'success', 'result': result})

if __name__ == '__main__':
    print('Starting AI Workspace Command Center UI on http://127.0.0.1:5000')
    app.run(host='127.0.0.1', port=5000)
