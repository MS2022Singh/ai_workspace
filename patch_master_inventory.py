import os
import json
import re

print('[+] Initializing Master OS Inventory Patch...')

# Create necessary directories
directories = ['catalog', 'ui/static', 'core/orchestrator']
for d in directories:
    os.makedirs(d, exist_ok=True)

# 1. Build the Unified Registry (LLMs, VLMs, Tools)
registry_data = {
    'models': [
        {'id': 'vllm-engine', 'name': 'VLLm High-Throughput', 'category': 'llm', 'active': False},
        {'id': 'ollama-local', 'name': 'Ollama Local Fleet', 'category': 'llm', 'active': False},
        {'id': 'qwen-3.8-local', 'name': 'Qwen 3.8 Local', 'category': 'llm', 'active': True},
        {'id': 'deepseek-reasonix', 'name': 'DeepSeek Reasonix', 'category': 'llm', 'active': False},
        {'id': 'wan2.2-vlm', 'name': 'Wan2.2 Vision Language', 'category': 'vlm', 'active': False},
        {'id': 'comfyui-engine', 'name': 'ComfyUI Image Gen', 'category': 'vlm', 'active': False},
        {'id': 'whisper-local', 'name': 'Whisper Audio', 'category': 'audio', 'active': False}
    ],
    'personas': [
        {'id': 'phd-researcher', 'prompt': 'Act as a PhD-level researcher. Base all output on real evidence and provide citations.'},
        {'id': 'expert-attorney', 'prompt': 'Act as an expert attorney. Draft documents with legal precision and cite relevant precedent.'},
        {'id': 'patent-drafter', 'prompt': 'Act as a patent drafter. Structure claims logically with technical exactness.'}
    ]
}

with open('catalog/registry.json', 'w') as f:
    json.dump(registry_data, f, indent=4)
print('[+] catalog/registry.json generated with extended LLM/VLM catalog.')

# 2. Patch the Frontend to include the Master Toggle and Dynamic Categories
frontend_patch = '''
<!-- INJECTED MASTER TOGGLE -->
<div class="master-toggle-container" style="padding: 10px; border-bottom: 1px solid #333; margin-bottom: 10px;">
    <label style="font-weight: bold; color: #00d2ff;">
        <input type="checkbox" id="master-toggle" onchange="toggleAllModels(this)"> 
        ACTIVATE ALL MODELS & TOOLS
    </label>
</div>
<script>
function toggleAllModels(masterCheckbox) {
    const toggles = document.querySelectorAll('.tool-toggle');
    toggles.forEach(toggle => {
        toggle.checked = masterCheckbox.checked;
        // Dispatch event to sync with backend
        toggle.dispatchEvent(new Event('change'));
    });
    console.log('Master Toggle Executed: All systems ' + (masterCheckbox.checked ? 'ONLINE' : 'OFFLINE'));
}
</script>
'''

# Assuming the main UI file is index.html in the root or templates folder
index_path = 'index.html'
if os.path.exists(index_path):
    with open(index_path, 'r') as f:
        html_content = f.read()
    
    if 'id="master-toggle"' not in html_content:
        # Insert right after the Master Tool Registry header
        html_content = html_content.replace('Master Tool Registry', f'Master Tool Registry{frontend_patch}')
        with open(index_path, 'w') as f:
            f.write(html_content)
        print('[+] Frontend patched with Master Toggle functionality.')
else:
    print('[-] index.html not found in root, skipping frontend DOM injection. Ensure you are in the correct directory.')

# 3. Patch the FastAPI Router to handle Personas
main_app_path = 'main.py'
persona_router_code = '''
# INJECTED PERSONA ROUTER
import json
@app.post("/api/set_persona")
async def set_persona(persona_id: str):
    try:
        with open('catalog/registry.json', 'r') as f:
            registry = json.load(f)
        persona = next((p for p in registry['personas'] if p['id'] == persona_id), None)
        if persona:
            # Update working memory state
            return {"status": "success", "active_persona": persona['id'], "system_prompt": persona['prompt']}
        return {"status": "error", "message": "Persona not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
'''

if os.path.exists(main_app_path):
    with open(main_app_path, 'r') as f:
        main_content = f.read()
    
    if '/api/set_persona' not in main_content:
        with open(main_app_path, 'a') as f:
            f.write(persona_router_code)
        print('[+] main.py patched with dynamic Persona Routing engine.')

print('[+] Master OS Architecture Rectification Complete. Please restart Uvicorn.')
