class MediaCompressor:
    @staticmethod
    def compress_media(input_file: str, quality_level: int = 80) -> dict:
        return {
            "status": "success",
            "input_file": input_file,
            "quality_level": quality_level,
            "compressed_file": f"{input_file}.compressed"
        }

compressor = MediaCompressor()
