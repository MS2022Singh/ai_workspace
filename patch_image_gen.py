import re
from pathlib import Path

main_path = Path("main.py")
src = main_path.read_text(encoding="utf-8")

# Remove old generate/image and api/image blocks, replace with real ones
pattern = re.compile(
    r'@app\.post\("/api/generate/image"\).*?(?=@app\.post)',
    re.DOTALL
)

new_image_block = '''@app.post("/api/generate/image")
async def generate_image_endpoint(payload: UniversalPayload):
    import requests, base64, urllib.parse, time

    prompt = payload.get_text() or "cosmic nebula"
    style = payload.style or "photorealistic"

    # Pollinations.ai — free, no key required
    seed = int(time.time()) % 100000
    full_prompt = f"{prompt}, {style}, high detail, 8k"
    encoded = urllib.parse.quote(full_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true&seed={seed}"

    try:
        r = requests.get(url, timeout=90)
        r.raise_for_status()
        b64 = base64.b64encode(r.content).decode("utf-8")
        data_uri = f"data:image/png;base64,{b64}"
        return {
            "status": "success",
            "prompt": prompt,
            "style": style,
            "image": data_uri,
            "image_url": url,
            "response": "Image generated successfully.",
            "result": data_uri,
            "html": f'<img src="{data_uri}" style="max-width:100%;border-radius:8px;" />'
        }
    except Exception as e:
        return {
            "status": "error",
            "detail": str(e),
            "response": f"Image generation failed: {e}",
            "result": "error"
        }

'''

new_src, count = pattern.subn(new_image_block, src, count=1)
if count > 0:
    main_path.write_text(new_src, encoding="utf-8")
    print(f"PATCHED: /api/generate/image replaced with real Pollinations call")
else:
    print("ERROR: could not locate /api/generate/image block")
