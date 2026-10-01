from PIL import Image, ImageDraw, ImageFont
import io, base64

def generate_visual_artifact(text_prompt):
    img = Image.new('RGB', (512, 512), color=(30, 34, 42))
    d = ImageDraw.Draw(img)
    d.rectangle([20, 20, 492, 492], outline=(0, 200, 255), width=3)
    d.text((40, 240), f'Artifact Generated:\n{text_prompt[:40]}...', fill=(255, 255, 255))
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    b64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f'data:image/png;base64,{b64_str}'
