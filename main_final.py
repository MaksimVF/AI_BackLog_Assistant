



import os
from crewai import Crew, Task
from agents.input_classifier_agent import input_classifier_agent
from agents.modality_detector_agent import modality_detector_agent
from agents.text_processor_agent import text_processor_agent
from agents.audio_transcriber_agent import audio_transcriber_agent
from agents.video_analyzer_agent import video_analyzer_agent
from agents.image_analyzer_agent import image_analyzer_agent
from config import settings, env  # Импортируем конфигурацию
from logger import setup_logger, get_logger
from custom_exceptions import DataProcessingError, ConfigurationError

# Initialize loggers
setup_logger()
logger = get_logger()

# Try to set up ClickHouse logger, but handle connection errors
try:
    from clickhouse_logger import setup_clickhouse_logger
    ch_logger = setup_clickhouse_logger()
except Exception as e:
    logger.warning(f"ClickHouse logger not available: {e}")
    ch_logger = None

def process_data(input_data):
    """Process input data with error handling and logging."""
    try:
        if not input_data:
            raise DataProcessingError("Данные отсутствуют или пусты")

        # Validate input data structure
        if "type" not in input_data:
            raise DataProcessingError("Не указан тип данных")

        if input_data["type"] not in ["text", "audio", "video", "image"]:
            raise DataProcessingError(f"Неподдерживаемый тип данных: {input_data['type']}")

        logger.info(f"Обработка данных типа: {input_data['type']}")
        if ch_logger:
            ch_logger.log_to_clickhouse('INFO', f"Обработка данных типа: {input_data['type']}")

        # Simulate data processing
        result = f"Обработанные данные: {input_data['type']}"

        logger.info("Данные успешно обработаны")
        if ch_logger:
            ch_logger.log_to_clickhouse('INFO', 'Данные успешно обработаны')

        return result

    except DataProcessingError as e:
        logger.error(f"Ошибка обработки данных: {e}")
        if ch_logger:
            ch_logger.log_to_clickhouse('ERROR', f"Ошибка обработки данных: {e}", "DATA_ERROR")
        return None
    except Exception as e:
        logger.error(f"Неожиданная ошибка при обработке данных: {e}")
        if ch_logger:
            ch_logger.log_to_clickhouse('ERROR', f"Неожиданная ошибка: {e}", "UNEXPECTED_ERROR")
        return None

def main():
    try:
        logger.info("🚀 Запуск системы мультиагентов")
        if ch_logger:
            ch_logger.log_to_clickhouse('INFO', 'Запуск системы мультиагентов')

        print("🚀 Запуск системы мультиагентов")
        print("=" * 50)

        # Проверка конфигурации
        if not hasattr(settings, 'WEAVIATE_URL') or not settings.WEAVIATE_URL:
            raise ConfigurationError("Не настроен Weaviate URL")

        logger.info("Проверка конфигурации")
        print(f"📋 Конфигурация:")
        print(f"   - Weaviate URL: {settings.WEAVIATE_URL}")
        print(f"   - Redis URL: {settings.REDIS_URL}")
        print(f"   - Путь к видео: {settings.VIDEO_PATH}")
        print(f"   - Путь к аудио: {settings.AUDIO_PATH}")
        print(f"   - Путь к транскриптам: {settings.TRANSCRIPTS_PATH}")

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
            {"type": "audio", "file_path": str(settings.AUDIO_PATH / "example.mp3")},
            {"type": "video", "file_path": str(settings.VIDEO_PATH / "example.mp4")},
            {"type": "image", "file_path": str(settings.DATA_PATH / "example.jpg")}
        ]

        # Обработка каждого входного элемента
        for i, input_data in enumerate(test_inputs, 1):
            logger.info(f"Обработка входного элемента {i}: {input_data}")
            print(f"\n📦 Обработка входного элемента {i}: {input_data}")

            try:
                # Выполнение задачи
                result = crew.execute_task(
                    task=classification_task,
                    input_data=input_data
                )

                # Process the result
                processed_result = process_data(result)

                if processed_result:
                    logger.info(f"Успешный результат: {processed_result}")
                    print(f"✅ Результат: {processed_result}")
                else:
                    logger.warning(f"Обработка данных завершилась с ошибками для элемента {i}")

            except Exception as e:
                logger.error(f"Ошибка при выполнении задачи для элемента {i}: {e}")
                if ch_logger:
                    ch_logger.log_to_clickhouse('ERROR', f"Ошибка при выполнении задачи: {e}", 'TASK_ERROR')

        logger.info("Все входные данные обработаны")
        print("\n🎉 Все входные данные обработаны!")

    except ConfigurationError as e:
        logger.error(f"Ошибка конфигурации: {e}")
        if ch_logger:
            ch_logger.log_to_clickhouse('ERROR', f"Ошибка конфигурации: {e}", 'CONFIG_ERROR')
    except Exception as e:
        logger.error(f"Неожиданная ошибка в основном процессе: {e}")
        if ch_logger:
            ch_logger.log_to_clickhouse('ERROR', f"Неожиданная ошибка: {e}", 'MAIN_ERROR')

if __name__ == "__main__":
    main()



