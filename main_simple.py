




import os
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

        # Пример входных данных
        test_inputs = [
            {"type": "text", "content": "Это пример текста для анализа"},
            {"type": "audio", "file_path": "/path/to/audio.mp3"},
            {"type": "video", "file_path": "/path/to/video.mp4"},
            {"type": "image", "file_path": "/path/to/image.jpg"}
        ]

        # Обработка каждого входного элемента
        for i, input_data in enumerate(test_inputs, 1):
            logger.info(f"Обработка входного элемента {i}: {input_data}")
            print(f"\n📦 Обработка входного элемента {i}: {input_data}")

            # Process the result
            processed_result = process_data(input_data)

            if processed_result:
                logger.info(f"Успешный результат: {processed_result}")
                print(f"✅ Результат: {processed_result}")
            else:
                logger.warning(f"Обработка данных завершилась с ошибками для элемента {i}")

        logger.info("Все входные данные обработаны")
        print("\n🎉 Все входные данные обработаны!")

    except Exception as e:
        logger.error(f"Неожиданная ошибка в основном процессе: {e}")
        if ch_logger:
            ch_logger.log_to_clickhouse('ERROR', f"Неожиданная ошибка: {e}", 'MAIN_ERROR')

if __name__ == "__main__":
    main()




