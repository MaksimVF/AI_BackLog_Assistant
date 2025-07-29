from agents.input_classifier_agent import InputClassifierAgent
from crewai import Task, Crew

def main():
    # Initialize the agent
    classifier_agent = InputClassifierAgent

    # Create a task for file type detection
    file_detection_task = Task(
        description="Определи тип файла по его пути",
        expected_output="MIME тип и расширение файла",
        agent=classifier_agent
    )

    # Create a crew with the agent and task
    crew = Crew(
        agents=[classifier_agent],
        tasks=[file_detection_task],
        verbose=True
    )

    # Test with different file types
    test_files = [
        "document.pdf",
        "image.jpg",
        "audio.mp3",
        "video.mp4",
        "data.json",
        "unknown_file.abc"
    ]

    print("Тестирование FileTypeDetectorTool:")
    print("=" * 50)

    for file_path in test_files:
        print(f"\nАнализ файла: {file_path}")

        # Execute the task
        result = crew.execute_task(
            task=file_detection_task,
            input_data=file_path
        )

        print(f"Результат: {result}")

if __name__ == "__main__":
    main()
