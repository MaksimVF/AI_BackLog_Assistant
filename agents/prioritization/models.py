



"""
Data Models for Prioritization Agents
"""

from typing import TypedDict, Optional, List
from enum import Enum

class PriorityScore(TypedDict, total=False):
    """Structure for priority scoring results"""
    score_type: str  # "RICE" or "ICE"
    score: float
    impact: int
    reach: Optional[int]
    confidence: float
    effort: int

class PriorityResult(TypedDict, total=False):
    """Structure for prioritization results"""
    task_id: str
    score: PriorityScore
    criticality: str
    is_bottleneck: bool
    bottlenecks: List[str]
    explanation: str
    reasoning: List[str]

class TaskData(TypedDict, total=False):
    """Structure for task input data"""
    task_id: str
    title: str
    description: str
    reach: Optional[int]
    impact: Optional[int]
    confidence: Optional[float]
    effort: Optional[int]
    urgency: Optional[int]
    is_blocking: Optional[bool]
    is_dependency: Optional[bool]
    blocks_count: Optional[int]
    dependencies: Optional[List[str]]



