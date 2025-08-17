



from datetime import datetime
from typing import List, Dict, Any
from ..dto import Task, AnalysisResult

class WeaviateRepository:
    def __init__(self, client: Any):
        self.client = client

    def fetch_tasks(self, project_id: str) -> List[Task]:
        # упрощённый пример (используйте GraphQL/nearText/filters)
        res = self.client.query.get("Task", ["id","project_id","title","description","tags","effort","reach","impact","confidence","dependencies","metadata","created_at"])\
            .with_where({"path":["project_id"], "operator":"Equal", "valueString":project_id}).do()
        tasks = []
        for obj in res['data']['Get']['Task']:
            tasks.append(Task(**obj))
        return tasks

    def save_analysis(self, result: AnalysisResult) -> None:
        # сохраняем в отдельный класс, например "AnalysisSnapshot"
        self.client.data_object.create({
            "project_id": result.project_id,
            "created_at": result.created_at.isoformat(),
            "payload": result.model_dump()
        }, class_name="AnalysisSnapshot")

    def update_task_labels(self, task_id: str, labels: dict) -> None:
        self.client.data_object.update({"labels": labels}, class_name="Task", uuid=task_id)



