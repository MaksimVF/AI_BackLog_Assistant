# Инициализация пакета агентов
# Здесь можно добавить общие импорты для агентов

from .aggregator_agent import AggregatorAgent
# from .input_classifier_agent import InputClassifierAgent
# from .reflection_agent import ReflectionAgent
from .reflection.document_reflection_agent import DocumentReflectionAgent
from .summary.summary_agent import SummaryAgent

__all__ = [
    "AggregatorAgent",
    # "InputClassifierAgent",
    # "ReflectionAgent",
    "DocumentReflectionAgent",
    "SummaryAgent"
]
