
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime

class VotingConfig(BaseModel):
    # минимальный % голосов для кворума (0..1)
    quorum_ratio: float = 0.5
    # порог согласия (доля голосов "за" относительно принявших участие)
    consensus_threshold: float = 0.6
    # вес по умолчанию для участников без явного веса
    default_weight: float = 1.0

class ConflictConfig(BaseModel):
    # порог, при превышении которого конфликт считается "high"
    severity_threshold: float = 0.6
    # коэффициент усиления важности при наличии нескольких конфликтующих стейкхолдеров
    multi_stakeholder_penalty: float = 0.2

class StakeholderAlignmentConfig(BaseModel):
    # порог совпадения целей/приоритетов для пометки "aligned"
    aligned_threshold: float = 0.7
    # относительная важность приоритета vs целей
    weight_priority: float = 0.6
    weight_goals: float = 0.4

# DTO для голосования
class Vote(BaseModel):
    voter_id: str
    value: Any                   # обычно: "yes"/"no"/"abstain" или числовая оценка
    weight: Optional[float] = None
    timestamp: Optional[datetime] = None

class VoteRequest(BaseModel):
    project_id: str
    task_id: str
    votes: List[Vote]
    vote_scheme: str = Field(default="binary")  # "binary"|"score"|"rank"

# Результат голосования
class VoteResult(BaseModel):
    task_id: str
    quorum: bool
    total_weight: float
    yes_weight: float
    no_weight: float
    abstain_weight: float
    consensus: bool
    decision: Optional[str] = None  # "approve"/"reject"/"no_consensus"
    breakdown: Dict[str, Any] = {}
