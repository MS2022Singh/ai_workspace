Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --reload-dir core --reload-dir ui
