import unittest
import sys
import os
sys.path.append(os.path.abspath("."))

from modules.audio.voice_engine import voice_engine
from modules.media.converter import media_converter
from core.permission_engine.policy_manager import policy_engine, PermissionClass

class TestVoiceAndMedia(unittest.TestCase):

    def test_voice_stt_tts_pipeline(self):
        policy_engine.set_permission(PermissionClass.READ, True)
        res_stt = voice_engine.process_audio_input(b"dummy_bytes")
        self.assertEqual(res_stt["status"], "success")
        self.assertIn("transcription", res_stt)

        res_tts = voice_engine.generate_speech_output("Test audio response")
        self.assertEqual(res_tts["status"], "success")

    def test_media_conversion_and_compression(self):
        policy_engine.set_permission(PermissionClass.WRITE, True)
        res_conv = media_converter.convert_format("sample.docx", "pdf")
        self.assertEqual(res_conv["status"], "success")
        self.assertEqual(res_conv["symbol_error_check"], "PASSED")

        res_comp = media_converter.compress_media("photo.jpg", "high")
        self.assertEqual(res_comp["status"], "success")

if __name__ == "__main__":
    unittest.main()
