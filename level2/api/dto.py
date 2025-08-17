

from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class StrategicAnalysisRequest(BaseModel):
    project_id: str
    task_ids: Optional[List[str]] = None
    methods: Optional[List[str]] = None  # если пусто → все агенты
    config: Optional[Dict[str, Any]] = None

class StrategicAnalysisResult(BaseModel):
    task_id: str
    method: str
    score: float
    labels: Dict[str, Any]
    details: Dict[str, Any]

