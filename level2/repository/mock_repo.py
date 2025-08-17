



from typing import List
from ..dto import Task, AnalysisResult
from ..interfaces import Repository

class MockRepository(Repository):
    def __init__(self):
        self.tasks = []
        self.saved_results = []

    def fetch_tasks(self, project_id: str) -> List[Task]:
        return [t for t in self.tasks if t.project_id == project_id]

    def save_analysis(self, result: AnalysisResult) -> None:
        self.saved_results.append(result)

    def update_task_labels(self, task_id: str, labels: dict) -> None:
        for task in self.tasks:
            if task.id == task_id:
                task.metadata.update(labels)
                break



