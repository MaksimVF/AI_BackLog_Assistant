


from agents.core_agent import CoreDocumentAgent

def process_video_task(video_path: str, source: str = "user_upload") -> bool:
    """
    Task function to process a video file.

    Args:
        video_path: Path to the video file
        source: Source of the upload

    Returns:
        bool: True if processing succeeded, False otherwise
    """
    agent = CoreDocumentAgent()
    return agent.process_video(video_path, source=source)


