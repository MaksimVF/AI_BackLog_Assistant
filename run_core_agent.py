

import argparse
from agents.core_agent import CoreDocumentAgent
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Агент обработки видеофайлов")
    parser.add_argument("video_path", type=str, help="Путь к видеофайлу")
    parser.add_argument("--source", type=str, default="user_upload", help="Источник загрузки")
    args = parser.parse_args()

    video_path = Path(args.video_path)
    if not video_path.exists():
        print(f"[ERROR] Файл {video_path} не найден.")
        return

    agent = CoreDocumentAgent()
    success = agent.process_video(str(video_path), source=args.source)

    if success:
        print("[SUCCESS] Обработка завершена успешно.")
    else:
        print("[FAIL] Обработка завершилась с ошибкой.")

if __name__ == "__main__":
    main()

