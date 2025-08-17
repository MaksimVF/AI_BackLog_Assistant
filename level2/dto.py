
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

class AnalysisConfig(BaseModel):
    methods: List[str] = Field(
        default_factory=lambda: ["RICE", "KANO", "MOSCOW", "WSJF", "RISK", "VALUE_EFFORT"]
    )
    weights: Dict[str, float] = Field(
        default_factory=lambda: {"RICE": 1.0, "KANO": 1.0, "MOSCOW": 0.7, "WSJF": 1.0, "RISK": 1.0, "VALUE_EFFORT": 0.8}
    )
    user_overrides: Dict[str, float] = {}  # переопределения параметров

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
