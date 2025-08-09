

"""
Main application with integrated monitoring and logging
"""

import os
import sys
import threading
import time
from crewai import Crew, Task
from agents.input_classifier_agent import input_classifier_agent
from agents.modality_detector_agent import modality_detector_agent
from agents.text_processor_agent import text_processor_agent
from agents.audio_transcriber_agent import audio_transcriber_agent
from agents.video_analyzer_agent import video_analyzer_agent
from agents.image_analyzer_agent import image_analyzer_agent

from config import settings_new as settings, env  # Импортируем новую конфигурацию
from utils.retry import RetryManager, retry
from utils.circuit_breaker import CircuitBreaker, circuit_breaker
from custom_exceptions import RetryableError, NonRetryableError

# Add project root to path for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize enhanced logging system
from agents.system_admin.logging_manager import initialize_logging
from agents.system_admin.monitoring_agent import MonitoringAgent
from health import get_health_status, get_readiness_status

# Initialize logging
logging_manager = initialize_logging(
    service_name="AI_BackLog_Assistant",
    environment=os.getenv('ENV', 'dev')
)
logger = logging_manager.get_logger()

# Initialize monitoring agent
monitoring_agent = MonitoringAgent()

def start_monitoring():
    """Start background monitoring"""
    def monitoring_loop():
        while True:
            try:
                # Get and log system status periodically
                status = monitoring_agent.get_system_status()
                logger.info("System status update", extra={
                    'cpu_usage': status.get('cpu', {}).get('percent', 0),
                    'memory_usage': status.get('memory', {}).get('virtual', {}).get('percent', 0),
                    'disk_usage': status.get('disk', {}).get('usage', {}).get('percent', 0)
                })

                # Sleep for 60 seconds
                time.sleep(60)
            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                time.sleep(10)

    # Start monitoring thread
    monitoring_thread = threading.Thread(
        target=monitoring_loop,
        daemon=True,
        name="SystemMonitoring"
    )
    monitoring_thread.start()
    logger.info("Started system monitoring")

def demonstrate_error_handling():
    """Demonstrate retry and circuit breaker functionality"""
    logger.info("🔄 Демонстрация механизмов обработки ошибок")
    print("\n🔄 Демонстрация механизмов обработки ошибок")
    print("-" * 50)

    # Demonstrate retry mechanism
    logger.info("🔁 Тестирование механизма повторных попыток")
    print("\n🔁 Тестирование механизма повторных попыток:")
    retry_manager = RetryManager(max_attempts=3, initial_delay=0.1)

    attempt_count = 0

    def unreliable_operation():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise RetryableError(f"Временная ошибка (попытка {attempt_count})")
        return f"✅ Успех после {attempt_count} попыток"

    try:
        result = retry_manager.call(unreliable_operation)
        logger.info(f"Retry result: {result}")
        print(f"   Результат: {result}")
    except Exception as e:
        logger.error(f"Retry failed: {e}")
        print(f"   Ошибка: {e}")

    # Demonstrate circuit breaker
    logger.info("🛡️  Тестирование механизма circuit breaker")
    print("\n🛡️  Тестирование механизма circuit breaker:")
    circuit_breaker = CircuitBreaker(
        name="demo-service",
        max_failures=2,
        reset_timeout=5
    )

    failure_count = 0

    def unreliable_service():
        nonlocal failure_count
        failure_count += 1
        if failure_count <= 2:
            raise RuntimeError(f"Сервисная ошибка {failure_count}")
        return f"✅ Сервис восстановлен (попытка {failure_count})"

    try:
        # First call should work
        result = circuit_breaker.call(unreliable_service)
        logger.info(f"Circuit breaker first call: {result}")
        print(f"   Первый вызов: {result}")
    except Exception as e:
        logger.error(f"Circuit breaker first call failed: {e}")
        print(f"   Первый вызов: Ошибка - {e}")

    try:
        # Second call should work
        result = circuit_breaker.call(unreliable_service)
        logger.info(f"Circuit breaker second call: {result}")
        print(f"   Второй вызов: {result}")
    except Exception as e:
        logger.error(f"Circuit breaker second call failed: {e}")
        print(f"   Второй вызов: Ошибка - {e}")

    try:
        # Third call should fail and open circuit
        result = circuit_breaker.call(unreliable_service)
        logger.info(f"Circuit breaker third call: {result}")
        print(f"   Третий вызов: {result}")
    except Exception as e:
        logger.error(f"Circuit breaker third call failed: {e}")
        print(f"   Третий вызов: Ошибка - {e}")

    try:
        # Fourth call should be blocked by circuit breaker
        result = circuit_breaker.call(unreliable_service)
        logger.info(f"Circuit breaker fourth call: {result}")
        print(f"   Четвёртый вызов: {result}")
    except Exception as e:
        logger.error(f"Circuit breaker fourth call failed: {e}")
        print(f"   Четвёртый вызов: Ошибка - {e}")

    logger.info(f"Circuit breaker state: {circuit_breaker.state}")
    print("   Состояние circuit breaker:", circuit_breaker.state)

def main():
    """Main application function"""
    logger.info("🚀 Запуск системы мультиагентов")
    print("🚀 Запуск системы мультиагентов")
    print("=" * 50)

    # Start monitoring
    start_monitoring()

    # Проверка конфигурации
    logger.info(f"📋 Конфигурация: Weaviate URL: {settings.WEAVIATE_URL}")
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
        logger.info(f"📦 Обработка входного элемента {i}: {input_data}")
        print(f"\n📦 Обработка входного элемента {i}: {input_data}")

        # Выполнение задачи
        result = crew.execute_task(
            task=classification_task,
            input_data=input_data
        )

        logger.info(f"✅ Результат: {result}")
        print(f"✅ Результат: {result}")

    logger.info("🎉 Все входные данные обработаны!")
    print("\n🎉 Все входные данные обработаны!")

    # Demonstrate error handling features
    demonstrate_error_handling()

    # Log final system health
    health = get_health_status()
    logger.info("Final system health", extra={
        'health_status': health['status'],
        'cpu_usage': health['system']['cpu_usage'],
        'memory_usage': health['system']['memory_usage'],
        'disk_usage': health['system']['disk_usage']
    })

if __name__ == "__main__":
    main()

