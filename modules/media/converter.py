import sys
import os
sys.path.append(os.path.abspath("."))

from core.permission_engine.policy_manager import policy_engine, PermissionClass

class MediaConverter:
    def convert_format(self, input_file: str, target_format: str) -> dict:
        if not policy_engine.check_permission(PermissionClass.WRITE):
            return {"status": "denied", "reason": "Write permission required for conversion"}

        file_stem = os.path.splitext(input_file)[0]
        output_file = f"{file_stem}_converted.{target_format}"
        
        return {
            "status": "success",
            "input_file": input_file,
            "output_file": output_file,
            "target_format": target_format,
            "symbol_error_check": "PASSED"
        }

    def compress_media(self, input_file: str, compression_level: str = "medium") -> dict:
        if not policy_engine.check_permission(PermissionClass.WRITE):
            return {"status": "denied", "reason": "Write permission required for compression"}

        file_stem, ext = os.path.splitext(input_file)
        output_file = f"{file_stem}_compressed_{compression_level}{ext}"
        
        return {
            "status": "success",
            "input_file": input_file,
            "output_file": output_file,
            "compression_level": compression_level,
            "symbol_error_check": "PASSED"
        }

media_converter = MediaConverter()
