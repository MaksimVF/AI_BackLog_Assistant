from tools.transcribe_audio import AudioTranscriptionTool

def test_audio_transcription():
    # Create the tool
    transcriber = AudioTranscriptionTool()

    # Test with a sample audio file (you'll need to provide a real audio file for testing)
    test_audio_file = "sample_audio.mp3"  # Replace with a real file path

    try:
        print("🎤 Testing audio transcription...")
        result = transcriber._run(test_audio_file)
        print(f"✅ Transcription result: {result}")
        return result
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        return None

if __name__ == "__main__":
    test_audio_transcription()
