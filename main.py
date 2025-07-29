from crewai import Crew, Task
from agents.input_classifier_agent import input_classifier_agent
from agents.modality_detector_agent import modality_detector_agent
from agents.text_processor_agent import text_processor_agent
from agents.audio_transcriber_agent import audio_transcriber_agent
from agents.video_analyzer_agent import video_analyzer_agent
from agents.image_analyzer_agent import image_analyzer_agent

def main():
    print("🚀 Запуск системы мультиагентов")
    print("=" * 50)

    # Создаём команду агентов
    agents = [
        input_classifier_agent,
        modality_detector_agent,
        text_processor_agent,
        audio_transcriber_agent,
        video_analyzer_agent,
        image_analyzer_agent
    ]

    # Создаём команду
    crew = Crew(
        agents=agents,
        verbose=True
    )

    # Пример задачи: классификация входных данных
    classification_task = Task(
        description="""
            Проанализировать входные данные и определить их модальность.
            В зависимости от типа данных, передать их соответствующему агенту для обработки.
        """,
        expected_output="Структурированный результат с типом данных и извлечённой информацией",
        agent=input_classifier_agent
    )

    # Пример входных данных
    test_inputs = [
        {"type": "text", "content": "Это пример текста для анализа"},
        {"type": "audio", "file_path": "example.mp3"},
        {"type": "video", "file_path": "example.mp4"},
        {"type": "image", "file_path": "example.jpg"}
    ]

    # Обработка каждого входного элемента
    for i, input_data in enumerate(test_inputs, 1):
        print(f"\n📦 Обработка входного элемента {i}: {input_data}")

        # Выполнение задачи
        result = crew.execute_task(
            task=classification_task,
            input_data=input_data
        )

        print(f"✅ Результат: {result}")

    print("\n🎉 Все входные данные обработаны!")

if __name__ == "__main__":
    main()
