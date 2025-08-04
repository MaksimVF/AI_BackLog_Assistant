

import os
from crewai import Crew, Task
from agents.pipeline_coordinator_agent import PipelineCoordinatorAgent
from agents.input_classifier_agent import input_classifier_agent
from agents.text_processor_agent import text_processor_agent
from agents.audio_transcriber_agent import audio_transcriber_agent
from agents.video_analyzer_agent import video_analyzer_agent
from agents.image_analyzer_agent import image_analyzer_agent
from config import settings, env  # Импортируем конфигурацию

def main():
    print("🚀 Запуск обновлённой системы мультиагентов")
    print("=" * 50)

    # Проверка конфигурации
    print(f"📋 Конфигурация:")
    print(f"   - Weaviate URL: {settings.WEAVIATE_URL}")
    print(f"   - Redis URL: {settings.REDIS_URL}")
    print(f"   - Путь к видео: {settings.VIDEO_PATH}")
    print(f"   - Путь к аудио: {settings.AUDIO_PATH}")
    print(f"   - Путь к транскриптам: {settings.TRANSCRIPTS_PATH}")

    # Создаём новый PipelineCoordinatorAgent
    pipeline_coordinator = PipelineCoordinatorAgent()

    # Создаём команду агентов с новым координатором
    agents = [
        input_classifier_agent,
        pipeline_coordinator,  # Используем новый объединённый агент
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

    # Пример задачи с использованием PipelineCoordinator
    coordination_task = Task(
        description="""
            Обработать текстовые данные через полный конвейер с маршрутизацией и агрегацией.
        """,
        expected_output="Полный анализ документа с маршрутизацией и рекомендациями",
        agent=pipeline_coordinator
    )

    # Пример входных данных
    test_inputs = [
        {"type": "text", "content": "Это пример текста для анализа"},
        {"type": "audio", "file_path": str(settings.AUDIO_PATH / "example.mp3")},
        {"type": "video", "file_path": str(settings.VIDEO_PATH / "example.mp4")},
        {"type": "image", "file_path": str(settings.DATA_PATH / "example.jpg")}
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

    # Дополнительный тест с PipelineCoordinator
    print("\n🧪 Тестирование PipelineCoordinatorAgent...")
    contract_text = """
    Настоящий договор аренды заключён между ООО "Ромашка" и ИП Иванов И.И.
    Сумма аренды: 50000 руб. в месяц. Срок: с 15.07.2023 по 15.07.2024.
    Контактный телефон: 8 (495) 123-45-67, email: contact@romashka.ru
    """

    # Прямое использование PipelineCoordinator
    pipeline_result = pipeline_coordinator.process("text", contract_text)
    print(f"📄 Обработанный текст: {pipeline_result['cleaned_text'][:100]}...")
    print(f"🤖 Рекомендованный агент: {pipeline_result['agent_name']}")
    print(f"📊 Результаты анализа: {pipeline_result['reflection_results']['summary']['summary']}")

    print("\n🎉 Все тесты завершены успешно!")

if __name__ == "__main__":
    main()

