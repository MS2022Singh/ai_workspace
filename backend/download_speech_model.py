"""
Downloads the small (~50MB) free, offline Vosk English speech model used
for local voice input, and extracts it to ~/.ai_workspace/vosk-model.

Run once via "Download Speech Model.bat". Safe to re-run.
"""
import io
import sys
import zipfile
from pathlib import Path
from urllib.request import urlopen

MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
DEST = Path.home() / ".ai_workspace" / "vosk-model"


def main():
    if DEST.exists() and any(DEST.iterdir()):
        print(f"Model already present at {DEST} -- nothing to do.")
        return

    print(f"Downloading speech model from:\n  {MODEL_URL}")
    print("(About 50MB -- this is a one-time download.)")
    try:
        with urlopen(MODEL_URL, timeout=60) as resp:
            data = resp.read()
    except Exception as e:
        print(f"\nDownload failed: {e}")
        print(
            "If your network blocks this, you can download the zip manually "
            f"from {MODEL_URL} and extract it so that its contents sit "
            f"directly inside:\n  {DEST}"
        )
        sys.exit(1)

    print("Extracting...")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        names = zf.namelist()
        top_level = names[0].split("/")[0] if names else ""
        zf.extractall(DEST.parent)

    extracted_dir = DEST.parent / top_level
    if extracted_dir.exists() and extracted_dir != DEST:
        extracted_dir.rename(DEST)

    print(f"Done. Speech model ready at {DEST}")


if __name__ == "__main__":
    main()
