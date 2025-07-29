









import os
from tools.audio2text_tool import AudioToTextTool
from tools.weaviate_storage_tool import WeaviateStorageTool

def transcribe_audio_file(audio_path):
    if not os.path.exists(audio_path):
        return {"error": "Audio file not found"}

    # Transcribe audio
    audio_to_text = AudioToTextTool()
    transcription = audio_to_text._execute(audio_path)

    # Store results in Weaviate
    weaviate = WeaviateStorageTool()
    weaviate.store_chunk(
        content=transcription,
        source_type="audio",
        source_name=os.path.basename(audio_path),
        metadata={"type": "transcription"}
    )

    return {
        "audio_path": audio_path,
        "transcription_length": len(transcription),
        "status": "processed"
    }










