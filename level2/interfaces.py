

from abc import ABC, abstractmethod
from typing import List
from .dto import Task, AnalysisResult, AnalysisConfig

class Repository(ABC):
    @abstractmethod
    def fetch_tasks(self, project_id: str) -> List[Task]: ...

    @abstractmethod
    def save_analysis(self, result: AnalysisResult) -> None: ...

    @abstractmethod
    def update_task_labels(self, task_id: str, labels: dict) -> None: ...

class ScoringAgent(ABC):
    name: str

    @abstractmethod
    def score(self, task: Task, cfg: AnalysisConfig) -> tuple[float, dict, dict]:
        """
        return: (score, details, labels)
        labels — опциональные категориальные метки (например, Kano class или MoSCoW label)
        """

