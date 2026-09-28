class FormatConverter:
    @staticmethod
    def convert_format(input_file: str, target_format: str) -> dict:
        return {
            "status": "success",
            "input_file": input_file,
            "target_format": target_format,
            "output_file": f"{input_file}.converted.{target_format}"
        }

converter = FormatConverter()
