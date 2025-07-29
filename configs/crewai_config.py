# CrewAI Configuration

# Default settings for CrewAI agents
DEFAULT_AGENT_SETTINGS = {
    "verbose": True,
    "allow_delegation": True,
    "max_iterations": 5,
    "temperature": 0.7
}

# Tool configuration
TOOL_CONFIG = {
    "file_type_detector": {
        "enabled": True,
        "priority": 1
    },
    "transcribe_audio": {
        "enabled": True,
        "priority": 2
    },
    "run_ocr": {
        "enabled": True,
        "priority": 3
    },
    "extract_frames": {
        "enabled": True,
        "priority": 4
    },
    "extract_text_from_pdf": {
        "enabled": True,
        "priority": 5
    }
}
