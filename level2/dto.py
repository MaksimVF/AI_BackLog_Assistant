
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class Task(BaseModel):
    id: str
    project_id: str
    title: str
    description: Optional[str] = None
    tags: List[str] = []
    effort: Optional[float] = None  # story points / hours
    reach: Optional[float] = None
    impact: Optional[float] = None
    confidence: Optional[float] = None
    dependencies: List[str] = []
    created_at: datetime
    metadata: Dict[str, str] = {}



class RiceConfig(BaseModel):
    # якоря для Impact (как у Intercom): tiny=0.25, low=0.5, medium=1.0, high=2.0, massive=3.0
    impact_anchors: Dict[str, float] = Field(
        default_factory=lambda: {"tiny": 0.25, "low": 0.5, "medium": 1.0, "high": 2.0, "massive": 3.0}
    )
    # нормализация Reach к интервалу [0..1] по заданным границам (например, пользователей в период)
    reach_min: float = 0.0
    reach_max: float = 10000.0
    # Effort в человеко-днях по умолчанию
    default_effort: float = 1.0
    # использовать PERT для Effort, если есть *_o, *_m, *_p
    use_effort_pert: bool = True
    # множитель штрафа за риск (если есть risk_prob/impact)
    risk_penalty: float = 0.0  # 0..1 (0 — не учитывать)

class WsjfConfig(BaseModel):
    # шкалы для нормализации компонент WSJF (1..10)
    min_score: float = 1.0
    max_score: float = 10.0
    # веса компонент (опционально)
    weight_bv: float = 1.0         # Business Value
    weight_tc: float = 1.0         # Time Criticality
    weight_rr_oe: float = 1.0      # Risk Reduction / Opportunity Enablement
    # job_size из effort (PERT при наличии)
    use_effort_pert: bool = True
    default_effort: float = 1.0

class KanoConfig(BaseModel):
    # веса влияния категорий на итоговую «полезность» (для численного score)
    weight_must_be: float = 0.9
    weight_performance: float = 1.0
    weight_attractive: float = 1.1
    weight_indifferent: float = 0.4
    weight_reverse: float = 0.0
    # коэффициенты индексов удовлетворенности
    alpha_cs: float = 0.6  # Customer Satisfaction (CS)
    beta_ds: float = 0.4   # Dissatisfaction (DS)

class MoscowConfig(BaseModel):
    base_weights: Dict[str, float] = Field(
        default_factory=lambda: {"must": 1.0, "should": 0.8, "could": 0.5, "wont": 0.0}
    )
    # корректировки
    dependency_boost: float = 0.1       # прибавка к score при критических зависимостях
    deadline_boost: float = 0.1         # при близком дедлайне
    capacity_penalty: float = 0.1       # штраф при нехватке ёмкости спринта
    # порог близости дедлайна (в днях)
    deadline_days_threshold: int = 14

class AnalysisConfig(BaseModel):


    methods: List[str] = Field(
        default_factory=lambda: ["RICE", "KANO", "MOSCOW", "WSJF"]
    )
    weights: Dict[str, float] = Field(
        default_factory=lambda: {"RICE": 1.0, "KANO": 1.0, "MOSCOW": 0.7, "WSJF": 1.0}
    )
    user_overrides: Dict[str, float] = {}  # переопределения параметров
    rice: RiceConfig = RiceConfig()
    wsjf: WsjfConfig = WsjfConfig()
    kano: KanoConfig = KanoConfig()
    moscow: MoscowConfig = MoscowConfig()

class MethodScore(BaseModel):
    method: str
    score: float
    details: Dict[str, Any] = {}

class TaskAnalysis(BaseModel):
    task_id: str
    method_scores: List[MethodScore]
    combined_score: float
    labels: Dict[str, str] = {}  # напр. { "KANO": "delighter", "MOSCOW": "should" }

class AnalysisResult(BaseModel):
    project_id: str
    tasks: List[TaskAnalysis]
    created_at: datetime
    config_used: AnalysisConfig
