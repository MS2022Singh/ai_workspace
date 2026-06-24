"""
Optional at-rest encryption for everything stored in the local database.

The key never leaves the machine and is never sent anywhere. This is
defense-in-depth for the SQLite file on disk (e.g. if the machine is shared
or backed up to a sync folder) -- it has nothing to do with model calls,
which already never leave the machine because they go to a local Ollama
server only.
"""
import secrets
from pathlib import Path
from cryptography.fernet import Fernet

KEY_PATH = Path.home() / ".ai_workspace" / "local.key"


def _get_key():
    KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not KEY_PATH.exists():
        KEY_PATH.write_bytes(Fernet.generate_key())
        try:
            # Best-effort: restrict permissions on POSIX. No-op on Windows.
            KEY_PATH.chmod(0o600)
        except Exception:
            pass
    return KEY_PATH.read_bytes()


def encrypt(plaintext: str) -> str:
    f = Fernet(_get_key())
    return "ENC::" + f.encrypt(plaintext.encode("utf-8")).decode("utf-8")


def decrypt(value: str) -> str:
    if not isinstance(value, str) or not value.startswith("ENC::"):
        return value
    f = Fernet(_get_key())
    return f.decrypt(value[len("ENC::"):].encode("utf-8")).decode("utf-8")


def generate_code() -> str:
    """A short code phones must supply to use this app over the LAN."""
    return f"{secrets.randbelow(1_000_000):06d}"
