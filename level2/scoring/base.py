

from __future__ import annotations
from typing import Tuple, Dict, Any, Protocol
from ..dto import Task, AnalysisConfig

class BaseScoringAgent(Protocol):
    """Контракт скорингового агента второго уровня."""
    name: str  # уникальное имя метода, например "RICE", "WSJF"

    def score(self, task: Task, cfg: AnalysisConfig) -> Tuple[float, Dict[str, Any], Dict[str, str]]:
        """
        Возвращает:
          - score: float — численная оценка (чем выше, тем приоритетнее)
          - details: Dict — подробности расчёта (для аудита/визуализации)
          - labels: Dict — категориальные метки/«корзины»
        """
        ...

