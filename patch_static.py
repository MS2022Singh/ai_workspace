import re
from pathlib import Path
main_path = Path("main.py")
src = main_path.read_text(encoding="utf-8")

if "StaticFiles" not in src and "app.mount" not in src:
    # Add static mount after CORS middleware
    marker = 'app.add_middleware('
    # Find end of CORS block
    idx = src.find(')\n', src.find('app.add_middleware('))
    insert_at = src.find('\n', idx) + 1
    addition = '''
from fastapi.staticfiles import StaticFiles
app.mount("/ui", StaticFiles(directory="ui"), name="ui")

'''
    src = src[:insert_at] + addition + src[insert_at:]
    main_path.write_text(src, encoding="utf-8")
    print("PATCHED: mounted ui/ as static files")
else:
    print("SKIP: static mount already present")
