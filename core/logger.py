import traceback, time, os, json

LOG_DIR = r'C:\AI_Workspace\ai_workspace_core\logs\errors'

def log_exception(error: Exception, context: str = ''):
    os.makedirs(LOG_DIR, exist_ok=True)
    log_entry = {
        'timestamp': time.time(),
        'context': context,
        'error': str(error),
        'traceback': traceback.format_exc()
    }
    filename = os.path.join(LOG_DIR, f'error_{int(time.time())}.json')
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(log_entry, f, indent=2)
    return filename
