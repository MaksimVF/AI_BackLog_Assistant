



import json
import redis
from deep_analysis_pipeline_v3 import DeepAnalysisPipeline

# Настройка Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Тестовая функция
def test_deep_analysis_pipeline():
    # Очистка очереди перед тестом
    redis_client.delete('analysis_queue')

    # Добавление тестовой задачи в очередь
    test_task = {
        "id": 1,
        "name": "Test Task",
        "importance": 7,
        "satisfaction": 8,
        "dissatisfaction": 2
    }
    redis_client.rpush('analysis_queue', json.dumps(test_task))

    # Создание и запуск конвейера
    pipeline = DeepAnalysisPipeline()
    task = pipeline.get_task_from_queue()

    if task:
        result = pipeline.process_task(task)
        print("Test Result:", json.dumps(result, indent=2))

        # Проверка результатов
        assert result['priority'] == 'high', "Priority should be high"
        assert result['moscow'] == 'must', "MoSCoW should be must"
        assert result['kano'] == 'attractive', "Kano should be attractive"
        assert result['analysis'] == 'completed', "Analysis should be completed"

        print("All tests passed!")
    else:
        print("No tasks in the queue")

# Запуск теста
if __name__ == "__main__":
    test_deep_analysis_pipeline()



