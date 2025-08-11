# tools/extract_frames.py

import os
import cv2
from crewai_tools import BaseTool

class ExtractFramesTool(BaseTool):
    name = "extract_frames"
    description = "Извлекает кадры из видео файла через заданные интервалы"

    def _run(self, video_file_path: str, output_dir: str = "frames", frame_interval_sec: int = 5) -> str:
        """
        Extract frames from video at specified intervals.

        Args:
            video_file_path: Path to input video file
            output_dir: Directory to save extracted frames
            frame_interval_sec: Interval in seconds between frames

        Returns:
            Path to output directory with extracted frames
        """
        if not os.path.exists(video_file_path):
            return f"Ошибка: Видео не найдено: {video_file_path}"

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        cap = cv2.VideoCapture(video_file_path)
        if not cap.isOpened():
            return f"Ошибка: Не удалось открыть видео: {video_file_path}"

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 25  # Default fallback

        frame_interval = int(fps * frame_interval_sec)
        frame_count = 0
        saved_count = 0
        frames = []

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

        return f"Извлечено {len(frames)} кадров в {output_dir}"
