




















from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class AgentConfig(BaseModel):
    name: str
    enabled: bool = True
    params: Dict[str, Any] = {}

class PipelineConfig(BaseModel):
    name: str
    agents: List[AgentConfig]
    params: Dict[str, Any] = {}

class SystemConfig(BaseModel):
    pipelines: List[PipelineConfig]

# Пример конфигурации по умолчанию
DEFAULT_CONFIG = SystemConfig(
    pipelines=[
        PipelineConfig(
            name="first_level",
            agents=[
                AgentConfig(name="modality_processing", enabled=True),
                AgentConfig(name="data_manipulation", enabled=True),
                AgentConfig(name="data_output", enabled=True),
                AgentConfig(name="second_level", enabled=True)
            ]
        ),
        PipelineConfig(
            name="second_level",
            agents=[
                AgentConfig(name="prioritization", enabled=True),
                AgentConfig(name="strategy", enabled=True),
                AgentConfig(name="teamwork", enabled=True),
                AgentConfig(name="analytics", enabled=True),
                AgentConfig(name="visualization", enabled=True)
            ]
        )
    ]
)























