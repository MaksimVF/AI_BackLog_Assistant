import mimetypes
from crewai_tools import BaseTool
from pathlib import Path

class FileTypeDetectorTool(BaseTool):
    name = "file_type_detector"
    description = "Определяет тип входного файла по расширению и MIME-типу"

    def _run(self, file_path: str) -> str:
        mime_type, _ = mimetypes.guess_type(file_path)
        suffix = Path(file_path).suffix.lower()

        if mime_type:
            return f"MIME: {mime_type}, Extension: {suffix}"
        else:
            return f"Extension: {suffix}, MIME: не удалось определить"
