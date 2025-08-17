






import json
from typing import Dict, List
from agents.moscow_agent import MoSCoWAgent
from agents.kano_agent import KanoAgent

# Базовый класс для агентов
class BaseAgent:
    def __init__(self, name: str):
        self.name = name

    def process(self, task: Dict) -> Dict:
        raise NotImplementedError("Метод process должен быть реализован в подклассе")

# Пример агента для приоритизации
class PriorityAgent(BaseAgent):
    def process(self, task: Dict) -> Dict:
        # Пример логики приоритизации
        task['priority'] = 'high' if task.get('importance', 0) > 5 else 'low'
        return task

# Пример агента для анализа
class AnalysisAgent(BaseAgent):
    def process(self, task: Dict) -> Dict:
        # Пример логики анализа
        task['analysis'] = 'completed'
        return task

# Конвейер второго уровня
class DeepAnalysisPipeline:
    def __init__(self):
        self.agents = []

    def add_agent(self, agent: BaseAgent):
        self.agents.append(agent)

    def process_task(self, task: Dict) -> Dict:
        for agent in self.agents:
            task = agent.process(task)
        return task

    def get_task_from_queue(self) -> Dict:
        # Временно отключаем интеграцию с Redis для тестирования
        # Возвращаем тестовую задачу
        return {
            "id": 1,
            "name": "Test Task",
            "importance": 7,
            "satisfaction": 8,
            "dissatisfaction": 2
        }

    def save_task_to_weaviate(self, task: Dict):
        # Временно отключаем сохранение в Weaviate для тестирования
        print(f"Task {task['id']} would be saved to Weaviate")

# Пример использования
if __name__ == "__main__":
    # Создание конвейера
    pipeline = DeepAnalysisPipeline()

    # Добавление агентов
    pipeline.add_agent(PriorityAgent("PriorityAgent"))
    pipeline.add_agent(MoSCoWAgent())
    pipeline.add_agent(KanoAgent())
    pipeline.add_agent(AnalysisAgent("AnalysisAgent"))

    # Получение задачи из очереди
    task = pipeline.get_task_from_queue()
    if task:
        # Обработка задачи
        result = pipeline.process_task(task)
        print("Processed Task:", json.dumps(result, indent=2))

        # Сохранение результата в Weaviate
        pipeline.save_task_to_weaviate(result)
    else:
        print("No tasks in the queue")







