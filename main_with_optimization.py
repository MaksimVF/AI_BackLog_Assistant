



"""
Main application with integrated performance optimization
"""

import os
import sys
import threading
import time
import asyncio
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
from performance_optimizer import performance_optimizer
from health import get_health_status, get_readiness_status

# Initialize logging
logging_manager = initialize_logging(
    service_name="AI_BackLog_Assistant",
    environment=os.getenv('ENV', 'dev')
)
logger = logging_manager.get_logger()

# Initialize monitoring agent
monitoring_agent = MonitoringAgent()

def start_performance_monitoring():
    """Start background performance monitoring"""
    def monitoring_loop():
        while True:
            try:
                # Get and log performance metrics periodically
                performance = performance_optimizer.get_system_performance()
                logger.info("Performance metrics update", extra=performance)

                # Check for bottlenecks
                analysis = performance_optimizer.analyze_performance_bottlenecks()
                if analysis['bottlenecks']:
                    logger.warning(f"Performance bottlenecks detected: {len(analysis['bottlenecks'])}")

                # Get recommendations
                recommendations = performance_optimizer.get_optimization_recommendations()
                if recommendations['recommendations']:
                    for rec in recommendations['recommendations']:
                        if rec['type'] == 'critical':
                            logger.error(f"Critical performance issue: {rec['message']}")
                        elif rec['type'] == 'warning':
                            logger.warning(f"Performance warning: {rec['message']}")

                # Sleep for 60 seconds
                time.sleep(60)
            except Exception as e:
                logger.error(f"Performance monitoring loop error: {e}")
                time.sleep(10)

    # Start monitoring thread
    monitoring_thread = threading.Thread(
        target=monitoring_loop,
        daemon=True,
        name="PerformanceMonitoring"
    )
    monitoring_thread.start()
    logger.info("Started performance monitoring")

@performance_optimizer.cache_decorator(expires=300)
def process_input_data(input_data: dict) -> dict:
    """
    Process input data with caching

    Args:
        input_data: Input data to process

    Returns:
        Processed result
    """
    logger.info(f"Processing input data: {input_data['type']}")

    # This would be the actual processing logic
    # For demonstration, we'll just return a simple result
    result = {
        'status': 'success',
        'input_type': input_data['type'],
        'processed_at': time.time(),
        'result': f"Processed {input_data['type']} data"
    }

    return result

async def async_process_video(video_path: str) -> dict:
    """
    Process video asynchronously

    Args:
        video_path: Path to video file

    Returns:
        Processing result
    """
    logger.info(f"Processing video asynchronously: {video_path}")

    # Simulate async video processing
    await asyncio.sleep(1)  # Simulate I/O operation

    return {
        'status': 'success',
        'video_path': video_path,
        'processing_time': 1.0,
        'result': 'Video processing completed'
    }

async def async_process_audio(audio_path: str) -> dict:
    """
    Process audio asynchronously

    Args:
        audio_path: Path to audio file

    Returns:
        Processing result
    """
    logger.info(f"Processing audio asynchronously: {audio_path}")

    # Simulate async audio processing
    await asyncio.sleep(0.5)  # Simulate I/O operation

    return {
        'status': 'success',
        'audio_path': audio_path,
        'processing_time': 0.5,
        'result': 'Audio processing completed'
    }

async def process_media_files(test_inputs: list) -> list:
    """
    Process media files asynchronously

    Args:
        test_inputs: List of input data

    Returns:
        List of processing results
    """
    tasks = []

    for input_data in test_inputs:
        if input_data['type'] == 'video':
            tasks.append(performance_optimizer.async_task(
                async_process_video, input_data['file_path']
            ))
        elif input_data['type'] == 'audio':
            tasks.append(performance_optimizer.async_task(
                async_process_audio, input_data['file_path']
            ))
        else:
            # Process other types synchronously
            result = process_input_data(input_data)
            tasks.append(asyncio.to_thread(lambda: result))

    # Run all tasks concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Handle any exceptions
    processed_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"Processing failed for input {i}: {result}")
            processed_results.append({'status': 'error', 'error': str(result)})
        else:
            processed_results.append(result)

    return processed_results

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

async def main():
    """Main application function"""
    logger.info("🚀 Запуск системы мультиагентов с оптимизацией производительности")
    print("🚀 Запуск системы мультиагентов с оптимизацией производительности")
    print("=" * 70)

    # Start performance monitoring
    start_performance_monitoring()

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

    # Обработка каждого входного элемента с оптимизацией
    print("\n📦 Обработка входных данных с оптимизацией производительности:")
    print("-" * 60)

    # Process media files asynchronously
    async_results = await process_media_files(test_inputs)

    for i, result in enumerate(async_results, 1):
        if result['status'] == 'success':
            print(f"✅ Результат {i}: {result['result']}")
        else:
            print(f"❌ Ошибка {i}: {result.get('error', 'Unknown error')}")

    # Process text data with caching
    text_result = process_input_data(test_inputs[0])
    print(f"✅ Текстовый результат: {text_result['result']}")

    # Process the same text again (should use cache)
    text_result_cached = process_input_data(test_inputs[0])
    print(f"✅ Текстовый результат (из кэша): {text_result_cached['result']}")

    print("\n🎉 Все входные данные обработаны с оптимизацией!")

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

    # Log performance recommendations
    recommendations = performance_optimizer.get_optimization_recommendations()
    if recommendations['recommendations']:
        logger.info(f"Performance recommendations: {len(recommendations['recommendations'])}")
        for rec in recommendations['recommendations']:
            logger.info(f"Recommendation: {rec['message']} - {rec['action']}")

if __name__ == "__main__":
    asyncio.run(main())


