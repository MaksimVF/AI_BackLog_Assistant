



from typing import List, Dict, Any
from ..dto import Task, AnalysisConfig
from .purpose_alignment import PurposeAlignmentAgent
from .impact_mapping import ImpactMappingAgent
from .cost_of_delay import CostOfDelayAgent
from .roi import RoiAgent

class StrategicOrchestrator:

    def __init__(self):
        self.agents = {
            "PURPOSE_ALIGNMENT": PurposeAlignmentAgent(),
            "IMPACT_MAPPING": ImpactMappingAgent(),
            "COST_OF_DELAY": CostOfDelayAgent(),
            "ROI": RoiAgent()
        }

    async def run(self, tasks: List[Task], cfg: AnalysisConfig, methods: List[str] = None):
        results = []
        for task in tasks:
            for name, agent in self.agents.items():
                if methods and name not in methods:
                    continue
                score, details, labels = agent.score(task, cfg)
                results.append({
                    "task_id": task.id,
                    "method": name,
                    "score": score,
                    "details": details,
                    "labels": labels
                })
        return results


