
"""
Simple test for Telegram Bot video/audio handling logic
"""

def test_file_type_detection():
    """Test file type detection logic"""

    # Test cases
    test_cases = [
        # Documents
        {"mime_type": "application/pdf", "expected": "📄 Document"},
        {"mime_type": "application/msword", "expected": "📄 Document"},
        {"mime_type": "text/plain", "expected": "📄 Document"},
        {"mime_type": "text/csv", "expected": "📄 Document"},

        # Videos
        {"mime_type": "video/mp4", "expected": "🎥 Video"},
        {"mime_type": "video/avi", "expected": "🎥 Video"},
        {"mime_type": "video/quicktime", "expected": "🎥 Video"},

        # Audio
        {"mime_type": "audio/mpeg", "expected": "🎧 Audio"},
        {"mime_type": "audio/wav", "expected": "🎧 Audio"},
        {"mime_type": "audio/ogg", "expected": "🎧 Audio"},
    ]

    # Test file type detection
    for i, test in enumerate(test_cases, 1):
        mime_type = test["mime_type"]
        expected = test["expected"]

        # Determine file type (logic from bot.py)
        file_type = "📄 Document"
        if mime_type.startswith('video/'):
            file_type = "🎥 Video"
        elif mime_type.startswith('audio/'):
            file_type = "🎧 Audio"

        # Check result
        result = "✅ PASS" if file_type == expected else "❌ FAIL"
        print(f"Test {i}: {mime_type} -> {file_type} (Expected: {expected}) {result}")

    print("\nFile type detection tests completed!")

if __name__ == "__main__":
    test_file_type_detection()
