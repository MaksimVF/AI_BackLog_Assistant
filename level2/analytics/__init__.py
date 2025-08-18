





# Analytics module initialization
# Import agents for easy access
from .agents.trend_analysis import TrendAnalysisAgent
from .agents.risk_analysis import RiskAnalysisAgent
from .agents.dependency_mapping import DependencyMappingAgent
from .agents.effort_forecasting import EffortForecastingAgent
from .agents.forensic_analysis import ForensicAnalysisAgent

# Export agents
__all__ = [
    "TrendAnalysisAgent",
    "RiskAnalysisAgent",
    "DependencyMappingAgent",
    "EffortForecastingAgent",
    "ForensicAnalysisAgent"
]





