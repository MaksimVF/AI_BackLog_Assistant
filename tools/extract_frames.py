# tools/extract_frames.py

from crewai_tools import BaseTool

class ExtractFramesTool(BaseTool):
    name = "extract_frames"
    description = "Извлекает кадры из видео файла"

    def _run(self, video_file_path: str, output_dir: str = "frames") -> str:
        # TODO: Implement using OpenCV or moviepy
        return "Реализация будет добавлена позже"
