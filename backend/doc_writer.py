"""
Converts the team's plain-text/lightweight-markdown output into real,
native Office files (.docx/.xlsx/.pptx) instead of dumping raw text into a
file with that extension. This is intentionally a simple, readable-output
converter, not a full document-formatting engine -- it won't reproduce
complex original formatting from an uploaded file, but it produces a
clean, properly-structured native file that opens correctly in Word/
Excel/PowerPoint.

Convention the model is asked to follow in its <<<FILE: ...>>> content:
  # Heading 1        -> Word: Heading 1 / PowerPoint: new slide title
  ## Heading 2        -> Word: Heading 2
  - bullet / * bullet -> bullet list item
  1. item             -> numbered list item
  (blank line)        -> paragraph break
  plain text          -> normal paragraph
For spreadsheets, content is treated as CSV; an optional
"--- Sheet: Name ---" line starts a new sheet.
"""
import csv
import io
import re


def _docx_bytes(text: str) -> bytes:
    import docx
    doc = docx.Document()
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if line.startswith("### "):
            doc.add_heading(line[4:].strip(), level=3)
        elif line.startswith("## "):
            doc.add_heading(line[3:].strip(), level=2)
        elif line.startswith("# "):
            doc.add_heading(line[2:].strip(), level=1)
        elif re.match(r"^[-*]\s+", line):
            doc.add_paragraph(re.sub(r"^[-*]\s+", "", line), style="List Bullet")
        elif re.match(r"^\d+\.\s+", line):
            doc.add_paragraph(re.sub(r"^\d+\.\s+", "", line), style="List Number")
        else:
            doc.add_paragraph(line)
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


def _xlsx_bytes(text: str) -> bytes:
    import openpyxl
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    sheets = re.split(r"^---\s*Sheet:\s*(.+?)\s*---$", text, flags=re.MULTILINE)
    # re.split with a capturing group returns: [before, name1, body1, name2, body2, ...]
    if len(sheets) == 1:
        chunks = [("Sheet1", text)]
    else:
        chunks = []
        # sheets[0] is anything before the first "--- Sheet ---" marker; skip if blank
        it = sheets[1:]
        for i in range(0, len(it), 2):
            name = it[i].strip()[:31] or f"Sheet{i // 2 + 1}"
            body = it[i + 1] if i + 1 < len(it) else ""
            chunks.append((name, body))

    for name, body in chunks:
        ws = wb.create_sheet(title=name)
        reader = csv.reader(io.StringIO(body.strip()))
        for row in reader:
            ws.append(row)

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def _pptx_bytes(text: str) -> bytes:
    from pptx import Presentation
    prs = Presentation()
    title_layout = prs.slide_layouts[1]  # "Title and Content"

    slides = []
    current_title = None
    current_bullets = []

    def flush():
        if current_title is not None:
            slides.append((current_title, current_bullets[:]))

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("# ") or line.startswith("## "):
            flush()
            current_title = re.sub(r"^#+\s*", "", line).strip()
            current_bullets = []
        elif re.match(r"^[-*]\s+", line):
            current_bullets.append(re.sub(r"^[-*]\s+", "", line))
        elif line.strip():
            current_bullets.append(line.strip())
    flush()

    if not slides:
        slides = [("Untitled", [text.strip()])]

    for title, bullets in slides:
        slide = prs.slides.add_slide(title_layout)
        slide.shapes.title.text = title
        body = slide.placeholders[1].text_frame
        body.clear()
        if bullets:
            body.text = bullets[0]
            for b in bullets[1:]:
                p = body.add_paragraph()
                p.text = b

    buf = io.BytesIO()
    prs.save(buf)
    return buf.getvalue()


CONVERTERS = {
    "docx": _docx_bytes,
    "xlsx": _xlsx_bytes,
    "pptx": _pptx_bytes,
}


def convert_if_needed(filename: str, text_content: str):
    """Returns (bytes_or_None, was_converted). If the extension isn't one
    we natively generate, returns (None, False) and the caller should save
    the original text content unchanged."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    converter = CONVERTERS.get(ext)
    if not converter:
        return None, False
    try:
        return converter(text_content), True
    except Exception:
        # If conversion fails for any reason, fall back to saving the raw
        # text rather than losing the content entirely.
        return None, False
