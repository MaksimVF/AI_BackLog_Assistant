







import os
from tools.video_frame_extractor_tool import VideoFrameExtractorTool
from tools.video2text_tool import VideoToTextTool
from tools.weaviate_storage_tool import WeaviateStorageTool

def process_video_file(video_path):
    if not os.path.exists(video_path):
        return {"error": "Video file not found"}

    # Extract frames
    frame_extractor = VideoFrameExtractorTool()
    frames = frame_extractor._execute(video_path)

    # Extract audio and transcribe
    video_to_text = VideoToTextTool()
    transcription = video_to_text._execute(video_path)

    # Store results in Weaviate
    weaviate = WeaviateStorageTool()

    # Store transcription
    weaviate.store_chunk(
        content=transcription,
        source_type="video",
        source_name=os.path.basename(video_path),
        metadata={"type": "transcription"}
    )

    # Store frame information
    for frame_path in frames:
        weaviate.store_chunk(
            content=f"Frame from {os.path.basename(video_path)}",
            source_type="video_frame",
            source_name=os.path.basename(video_path),
            metadata={"frame_path": frame_path}
        )

    return {
        "video_path": video_path,
        "frames_extracted": len(frames),
        "transcription_length": len(transcription),
        "status": "processed"
    }








