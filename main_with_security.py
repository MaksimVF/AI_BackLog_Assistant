




"""
Main application with integrated security features
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
from security_integration import security_integration
from health import get_health_status, get_readiness_status

# Initialize logging
logging_manager = initialize_logging(
    service_name="AI_BackLog_Assistant",
    environment=os.getenv('ENV', 'dev')
)
logger = logging_manager.get_logger()

# Initialize monitoring agent
monitoring_agent = MonitoringAgent()

def start_security_monitoring():
    """Start background security monitoring"""
    security_integration.start_security_monitoring()
    logger.info("Started security monitoring")

@security_integration.secure_api_endpoint(required_security_level=SecurityLevel.MEDIUM)
def process_secure_input(input_data: dict, api_key: str = None, token: str = None) -> dict:
    """
    Process input data securely with API key or token authentication

    Args:
        input_data: Input data to process
        api_key: API key for authentication
        token: Authentication token

    Returns:
        Processed result
    """
    logger.info(f"Processing secure input: {input_data['type']}")

    # Audit the operation
    security_integration.audit_operation(
        "process_secure_input",
        inputs=input_data,
        status="success"
    )

    # This would be the actual processing logic
    # For demonstration, we'll just return a simple result
    result = {
        'status': 'success',
        'input_type': input_data['type'],
        'processed_at': time.time(),
        'result': f"Securely processed {input_data['type']} data"
    }

    return result

async def process_secure_media_files(test_inputs: list) -> list:
    """
    Process media files securely

    Args:
        test_inputs: List of input data

    Returns:
        List of processing results
    """
    tasks = []

    for input_data in test_inputs:
        # Secure each media processing operation
        secure_message = security_integration.secure_component_communication(
            input_data,
            "main_app",
            "media_processor"
        )

        # Process the secure message
        try:
            verified_data = security_integration.verify_component_message(
                secure_message,
                expected_source="main_app",
                expected_target="media_processor"
            )

            # Process the verified data
            result = {
                'status': 'success',
                'input_type': verified_data['type'],
                'processed_at': time.time(),
                'result': f"Securely processed {verified_data['type']} data"
            }

            tasks.append(asyncio.to_thread(lambda: result))

        except Exception as e:
            logger.error(f"Failed to process secure media: {e}")
            tasks.append(asyncio.to_thread(lambda: {
                'status': 'error',
                'error': str(e)
            }))

    # Run all tasks concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Handle any exceptions
    processed_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"Secure processing failed for input {i}: {result}")
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
    """Main application function with security integration"""
    logger.info("🚀 Запуск системы мультиагентов с улучшенной безопасностью")
    print("🚀 Запуск системы мультиагентов с улучшенной безопасностью")
    print("=" * 70)

    # Start security monitoring
    start_security_monitoring()

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

    # Обработка каждого входного элемента с безопасностью
    print("\n🔒 Обработка входных данных с улучшенной безопасностью:")
    print("-" * 60)

    # Process media files securely
    async_results = await process_secure_media_files(test_inputs)

    for i, result in enumerate(async_results, 1):
        if result['status'] == 'success':
            print(f"✅ Безопасный результат {i}: {result['result']}")
        else:
            print(f"❌ Ошибка безопасности {i}: {result.get('error', 'Unknown error')}")

    # Process text data securely
    text_result = process_secure_input(test_inputs[0])
    print(f"✅ Безопасный текстовый результат: {text_result['result']}")

    # Perform security audit
    audit_results = security_integration.perform_security_audit()
    print(f"\n🔍 Результаты аудита безопасности:")
    print(f"   - Рекомендации: {len(audit_results['recommendations'])}")
    print(f"   - Уязвимости: {len(audit_results.get('vulnerabilities', []))}")

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

    # Log security status
    security_audit = security_integration.perform_security_audit()
    logger.info("Security audit completed", extra={
        'recommendations': len(security_audit['recommendations']),
        'vulnerabilities': len(security_audit.get('vulnerabilities', []))
    })

if __name__ == "__main__":
    asyncio.run(main())




