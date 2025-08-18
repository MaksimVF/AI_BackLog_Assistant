




from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class TrendConfig(BaseModel):
    # период в днях для анализа тренда (скользящее окно)
    window_days: int = 30
    min_points: int = 3

class RiskConfig(BaseModel):
    # коэффициент чувствительности к историческим отказам
    failure_weight: float = 0.6
    dependency_weight: float = 0.3
    metadata_risk_weight: float = 0.1

class DependencyConfig(BaseModel):
    # глубина обхода зависимостей
    max_depth: int = 5

class EffortForecastConfig(BaseModel):
    # сколько прошлых спринтов/задач брать
    history_size: int = 10
    # минимальное количество исторических точек
    min_points: int = 3

class ForensicConfig(BaseModel):
    # пороги для выявления проблем (в долях)
    delay_threshold_ratio: float = 0.2  # задержка >20% считается значительной
    recurrence_threshold: int = 3       # количество повторений для выявления повторяющейся проблемы




