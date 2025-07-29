



import os
import cv2
import tempfile
from crewai_tools import BaseTool

class VideoFrameExtractorTool(BaseTool):
    name = "video_frame_extractor"
    description = "Извлекает кадры из видеофайла через заданные интервалы и сохраняет их во временную папку."

    def _execute(self, video_path: str, frame_interval_sec: int = 5) -> list:
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Видео не найдено: {video_path}")

        # Создание временной директории для кадров
        output_dir = tempfile.mkdtemp(prefix="frames_")
        frames = []

        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * frame_interval_sec)
        frame_count = 0
        saved_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % frame_interval == 0:
                frame_path = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
                cv2.imwrite(frame_path, frame)
                frames.append(frame_path)
                saved_count += 1
            frame_count += 1

        cap.release()
        return frames



