"""
Thin wrapper around a LOCAL Ollama server (http://localhost:11434).
No data ever leaves the machine through this module -- it is the only
place in the codebase that makes network calls, and it only ever talks
to localhost.
"""
import requests

OLLAMA_URL = "http://localhost:11434"


class OllamaError(Exception):
    pass


def is_running() -> bool:
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


def list_models():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        r.raise_for_status()
        data = r.json()
        return [m["name"] for m in data.get("models", [])]
    except Exception as e:
        raise OllamaError(f"Could not reach local Ollama server: {e}")


def chat(model: str, system: str, user: str, images: list = None, timeout: int = 300) -> str:
    """Single-turn chat call. Returns the assistant's reply text.
    `images`, if given, is a list of base64-encoded image strings (no data
    URI prefix) -- only meaningful with a vision-capable model."""
    user_message = {"role": "user", "content": user}
    if images:
        user_message["images"] = images
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": model,
                "stream": False,
                "messages": [
                    {"role": "system", "content": system},
                    user_message,
                ],
            },
            timeout=timeout,
        )
        if not r.ok:
            # Surface Ollama's own error message (e.g. "model 'X' not
            # found, try pulling it first") instead of a generic HTTP error.
            try:
                detail = r.json().get("error", r.text)
            except Exception:
                detail = r.text
            raise OllamaError(
                f"Ollama rejected the request for model '{model}': {detail}"
                + (
                    f"\n(Try: ollama pull {model})"
                    if "not found" in str(detail).lower()
                    else ""
                )
            )
        data = r.json()
        return data.get("message", {}).get("content", "").strip()
    except requests.exceptions.ConnectionError:
        raise OllamaError(
            "Could not reach Ollama at localhost:11434. Is Ollama installed and running?"
        )
    except OllamaError:
        raise
    except Exception as e:
        raise OllamaError(f"Ollama call failed for model '{model}': {e}")
