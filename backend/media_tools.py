"""
Local, deterministic media tools -- image editing, collage splitting,
logo generation, and slideshow/reel video. None of this calls any AI
model; it's plain image processing (Pillow), which is faster, more
predictable, and needs no GPU or multi-gigabyte downloads.

Optional enhanced features (smart/irregular collage detection, real AI
image generation) are intentionally NOT bundled here by default -- see
README "Media tools" section for how to add them if wanted.
"""
import io
import zipfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

# ---------- helpers ----------

_FONT_CANDIDATES = [
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\calibrib.ttf",
]


def _load_font(size: int):
    for path in _FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _to_png_bytes(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.convert("RGBA").save(buf, format="PNG")
    return buf.getvalue()


def _open(image_bytes: bytes) -> Image.Image:
    return Image.open(io.BytesIO(image_bytes))


# ---------- collage / grid splitting ----------

def split_grid(image_bytes: bytes, rows: int, cols: int):
    """Splits an image into rows*cols equal tiles. Returns a list of
    (filename, png_bytes) tuples. Works best on a regular grid collage --
    for irregular/overlapping layouts, see the README's optional smart
    splitter."""
    rows = max(1, int(rows))
    cols = max(1, int(cols))
    img = _open(image_bytes).convert("RGB")
    w, h = img.size
    cell_w = w / cols
    cell_h = h / rows
    tiles = []
    for r in range(rows):
        for c in range(cols):
            box = (
                round(c * cell_w),
                round(r * cell_h),
                round((c + 1) * cell_w),
                round((r + 1) * cell_h),
            )
            tile = img.crop(box)
            tiles.append((f"tile_r{r + 1}_c{c + 1}.png", _to_png_bytes(tile)))
    return tiles


def tiles_to_zip(tiles) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in tiles:
            zf.writestr(name, data)
    return buf.getvalue()


# ---------- general image editing ----------

def edit_image(image_bytes: bytes, operation: str, params: dict) -> bytes:
    img = _open(image_bytes)
    op = operation.lower()

    if op == "resize":
        w = int(params.get("width") or img.width)
        h = int(params.get("height") or img.height)
        img = img.resize((w, h), Image.LANCZOS)
    elif op == "crop":
        box = (
            int(params.get("left", 0)),
            int(params.get("top", 0)),
            int(params.get("right", img.width)),
            int(params.get("bottom", img.height)),
        )
        img = img.crop(box)
    elif op == "rotate":
        degrees = float(params.get("degrees", 90))
        img = img.rotate(-degrees, expand=True)
    elif op == "flip_h":
        img = ImageOps.mirror(img)
    elif op == "flip_v":
        img = ImageOps.flip(img)
    elif op == "grayscale":
        img = ImageOps.grayscale(img)
    elif op == "blur":
        radius = float(params.get("radius", 4))
        img = img.filter(ImageFilter.GaussianBlur(radius))
    elif op == "sharpen":
        img = img.filter(ImageFilter.SHARPEN)
    elif op == "brightness":
        factor = float(params.get("factor", 1.2))
        img = ImageEnhance.Brightness(img).enhance(factor)
    elif op == "contrast":
        factor = float(params.get("factor", 1.2))
        img = ImageEnhance.Contrast(img).enhance(factor)
    else:
        raise ValueError(f"Unknown operation: {operation}")

    target_format = (params.get("format") or "PNG").upper()
    if target_format == "JPG":
        target_format = "JPEG"
    save_img = img.convert("RGB") if target_format == "JPEG" else img.convert("RGBA")
    buf = io.BytesIO()
    save_img.save(buf, format=target_format)
    return buf.getvalue()


# ---------- logo generation ----------

LOGO_PALETTES = {
    "midnight": {"bg": (15, 23, 42), "accent": (242, 169, 59), "text": (231, 234, 238)},
    "fresh": {"bg": (16, 42, 31), "accent": (61, 214, 140), "text": (255, 255, 255)},
    "bold": {"bg": (44, 20, 22), "accent": (229, 72, 77), "text": (255, 255, 255)},
    "ocean": {"bg": (15, 35, 51), "accent": (79, 183, 255), "text": (255, 255, 255)},
    "minimal": {"bg": (245, 245, 245), "accent": (30, 30, 30), "text": (30, 30, 30)},
}


def generate_logo(text: str, subtext: str = "", palette: str = "midnight", size: int = 512) -> bytes:
    colors = LOGO_PALETTES.get(palette, LOGO_PALETTES["midnight"])
    img = Image.new("RGB", (size, size), colors["bg"])
    draw = ImageDraw.Draw(img)

    # A simple accent shape -- a rounded square "mark" -- behind/above the text.
    mark_size = size * 0.22
    mark_box = (size / 2 - mark_size / 2, size * 0.16, size / 2 + mark_size / 2, size * 0.16 + mark_size)
    draw.rounded_rectangle(mark_box, radius=mark_size * 0.22, fill=colors["accent"])

    main_font = _load_font(int(size * 0.11))
    sub_font = _load_font(int(size * 0.045))

    text = text.strip() or "LOGO"
    bbox = draw.textbbox((0, 0), text, font=main_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size - tw) / 2, size * 0.55), text, font=main_font, fill=colors["text"])

    if subtext.strip():
        bbox2 = draw.textbbox((0, 0), subtext, font=sub_font)
        sw = bbox2[2] - bbox2[0]
        draw.text(((size - sw) / 2, size * 0.72), subtext, font=sub_font, fill=colors["accent"])

    return _to_png_bytes(img)


# ---------- slideshow / reel ----------

def _fit_canvas(img: Image.Image, target_size):
    """Resizes to fit within target_size, padded with black bars (letterbox)."""
    img = img.convert("RGB")
    tw, th = target_size
    scale = min(tw / img.width, th / img.height)
    new_size = (max(1, int(img.width * scale)), max(1, int(img.height * scale)))
    resized = img.resize(new_size, Image.LANCZOS)
    canvas = Image.new("RGB", target_size, (0, 0, 0))
    canvas.paste(resized, ((tw - new_size[0]) // 2, (th - new_size[1]) // 2))
    return canvas


def make_slideshow_gif(images: list, seconds_per_slide: float = 2.0, size=(960, 540)) -> bytes:
    frames = [_fit_canvas(_open(b), size) for b in images]
    if not frames:
        raise ValueError("No images provided")
    buf = io.BytesIO()
    frames[0].save(
        buf,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=int(seconds_per_slide * 1000),
        loop=0,
    )
    return buf.getvalue()


def make_slideshow_mp4(images: list, seconds_per_slide: float = 2.0, size=(960, 540), fps: int = 24) -> bytes:
    """Requires opencv-python-headless. Raises a clear error if not installed."""
    try:
        import cv2
        import numpy as np
    except ImportError:
        raise RuntimeError(
            "MP4 export needs an optional extra package. Run "
            "'Install Media Tools (optional).bat' once, then try again. "
            "(GIF export works right now without it.)"
        )
    import tempfile
    import os

    frames = [_fit_canvas(_open(b), size) for b in images]
    if not frames:
        raise ValueError("No images provided")

    fd, path = tempfile.mkstemp(suffix=".mp4")
    os.close(fd)
    try:
        writer = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"mp4v"), fps, size)
        for frame in frames:
            arr = np.array(frame)[:, :, ::-1]  # RGB -> BGR
            for _ in range(int(fps * seconds_per_slide)):
                writer.write(arr)
        writer.release()
        with open(path, "rb") as f:
            return f.read()
    finally:
        try:
            os.remove(path)
        except OSError:
            pass
