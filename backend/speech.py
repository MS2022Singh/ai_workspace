"""
Local, fully offline speech-to-text using Vosk. No audio is ever sent
anywhere -- the model runs on this machine, just like the Ollama models do.

Requires a one-time model download (see README "Voice input" section, or
run "Download Speech Model.bat"). Until that model is present, transcribe()
raises a clear, actionable error rather than failing mysteriously.
"""
import io
import json
import wave
from pathlib import Path

MODEL_DIR = Path.home() / ".ai_workspace" / "vosk-model"

_model = None


def is_model_available() -> bool:
    return MODEL_DIR.exists() and any(MODEL_DIR.iterdir())


def _get_model():
    global _model
    if _model is None:
        if not is_model_available():
            return None
        from vosk import Model  # imported lazily; only needed if voice is used
        _model = Model(str(MODEL_DIR))
    return _model


def transcribe_wav_bytes(wav_bytes: bytes) -> str:
    model = _get_model()
    if model is None:
        raise RuntimeError(
            "No local speech model found. Run 'Download Speech Model.bat' "
            "once (or see the README's 'Voice input' section), then try "
            "again."
        )
    from vosk import KaldiRecognizer

    wf = wave.open(io.BytesIO(wav_bytes), "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
        raise RuntimeError("Expected mono 16-bit PCM WAV audio.")

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(False)
    chunks = []
    while True:
        data = wf.readframes(4000)
        if not data:
            break
        if rec.AcceptWaveform(data):
            piece = json.loads(rec.Result()).get("text", "")
            if piece:
                chunks.append(piece)
    final = json.loads(rec.FinalResult()).get("text", "")
    if final:
        chunks.append(final)
    return " ".join(chunks).strip()
