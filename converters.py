class MediaEngine:
    @staticmethod
    def convert_file(filename: str, source_type: str, target_format: str) -> dict:
        out_name = f"converted_{filename}.{target_format.lower()}"
        return {
            "status": "success",
            "filename": out_name,
            "message": f"Successfully converted {filename} ({source_type}) to {target_format.upper()}",
            "download_url": f"/static/{out_name}"
        }

    @staticmethod
    def compress_file(filename: str, compression_level: int, target_size_mb: float) -> dict:
        out_name = f"compressed_file"
        return {
            "status": "success",
            "filename": out_name,
            "message": f"Compressed by {compression_level}% (Target: {target_size_mb} MB)",
            "download_url": f"/static/{out_name}"
        }
