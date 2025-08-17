



import json
from deep_analysis_pipeline_v10 import DeepAnalysisPipeline

# Тестовая функция
def test_deep_analysis_pipeline():
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



