import sys
import os
import logging
sys.path.append(os.path.abspath("."))

from core.event_bus.pypubsub_router import event_bus
from core.permission_engine.policy_manager import policy_engine, PermissionClass

logger = logging.getLogger("VoiceEngine")

class VoiceEngine:
    def __init__(self, mode="hybrid"):
        self.mode = mode  # local or hybrid
        self.is_listening = False

    def process_audio_input(self, audio_chunk_bytes: bytes) -> dict:
        if not policy_engine.check_permission(PermissionClass.READ):
            return {"status": "denied", "reason": "Microphone/Read permission required"}

        # Simulated VAD (Voice Activity Detection) & Speech-to-Text transcription
        transcription = "Execute system health check"
        event_bus.publish("USER_SPOKE", {"text": transcription, "mode": self.mode})
        return {"status": "success", "transcription": transcription, "vad_active": True}

    def generate_speech_output(self, text: str) -> dict:
        # Simulated TTS (Text-to-Speech) generation
        audio_payload_path = f"output/tts_{hash(text)}.wav"
        return {"status": "success", "audio_path": audio_payload_path, "text": text}

voice_engine = VoiceEngine()
