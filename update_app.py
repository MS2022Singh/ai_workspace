with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

root_route = '''
from fastapi.responses import HTMLResponse

@app.get(\"/\", response_class=HTMLResponse)
async def read_root():
    return \"\"\"<!DOCTYPE html>
<html>
<head>
    <title>AI Workspace</title>
    <style>
        body { background: #1e1e1e; color: #ffffff; font-family: Arial, sans-serif; padding: 40px; margin: 0; }
        h1 { color: #4CAF50; }
        .card { background: #2d2d2d; padding: 20px; border-radius: 8px; margin-top: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        button { background: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-weight: bold; }
        button:hover { background: #45a049; }
        pre { background: #121212; padding: 15px; border-radius: 5px; overflow-x: auto; color: #a6e22e; }
    </style>
</head>
<body>
    <h1>AI Workspace Control Panel</h1>
    <div class=\"card\">
        <h3>API & System Status</h3>
        <pre id=\"status\">Loading system health...</pre>
        <button onclick=\"checkHealth()\">Refresh Status</button>
    </div>
    <script>
        async function checkHealth() {
            document.getElementById('status').innerText = 'Checking...';
            try {
                const res = await fetch('/api/health');
                const data = await res.json();
                document.getElementById('status').innerText = JSON.stringify(data, null, 2);
            } catch (e) {
                document.getElementById('status').innerText = 'Error: Unable to reach /api/health endpoint.';
            }
        }
        checkHealth();
    </script>
</body>
</html>\"\"\"
'''

if 'response_class=HTMLResponse' not in content:
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content + '\n' + root_route)
    print('Updated app.py successfully')
else:
    print('Root route already exists')
