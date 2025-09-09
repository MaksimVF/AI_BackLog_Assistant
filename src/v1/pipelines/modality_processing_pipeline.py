

















from typing import List, Dict, Any

class ModalityProcessingPipeline:
    """
    Конвейер обработки модальностей: очистка и нормализация данных.
    """

    def __init__(self):
        pass

    async def run(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Запуск конвейера обработки модальностей.
        :param tasks: список задач в формате словарей
        :return: очищенные и нормализованные задачи
        """
        # Пример очистки и нормализации данных
        cleaned_tasks = []
        for task in tasks:
            cleaned_task = {
                "id": task.get("id", ""),
                "title": task.get("title", "").strip(),
                "status": task.get("status", "").strip(),
                "value": float(task.get("value", 0)),
                "effort": float(task.get("effort", 0)),
                "dependencies": task.get("dependencies", []),
                "start_date": task.get("start_date", ""),
                "end_date": task.get("end_date", "")
            }
            cleaned_tasks.append(cleaned_task)
        return cleaned_tasks



















