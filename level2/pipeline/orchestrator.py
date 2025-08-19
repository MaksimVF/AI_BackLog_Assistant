


from datetime import datetime
from typing import List, Dict, Type
from ..dto import Task, AnalysisConfig, TaskAnalysis, MethodScore, AnalysisResult
from ..interfaces import Repository
from ..scoring.rice import RiceAgent
from ..scoring.moscow import MoSCoWAgent
from ..scoring.wsjf import WSJFAgent
from ..scoring.kano import KanoAgent
from ..scoring.value_vs_effort import ValueVsEffortAgent
from ..scoring.opportunity_scoring import OpportunityScoringAgent
from ..scoring.stack_ranking import StackRankingAgent
from ..aggregator.weigh_combiner import combine_scores

AGENTS_REGISTRY = {
    "RICE": RiceAgent(),
    "MOSCOW": MoSCoWAgent(),
    "WSJF": WSJFAgent(),
    "KANO": KanoAgent(),
    "VALUE_EFFORT": ValueVsEffortAgent(),
    "OPPORTUNITY": OpportunityScoringAgent(),
    "STACK_RANKING": StackRankingAgent(),
}

class Level2Orchestrator:
    def __init__(self, repo: Repository):
        self.repo = repo

    def analyze_project(self, project_id: str, cfg: AnalysisConfig) -> AnalysisResult:
        tasks: List[Task] = self.repo.fetch_tasks(project_id)
        analyzed: List[TaskAnalysis] = []

        for t in tasks:
            method_scores = []
            labels_agg: Dict[str, str] = {}

            for method in cfg.methods:
                agent = AGENTS_REGISTRY.get(method.upper())
                if not agent:
                    continue
                score, details, labels = agent.score(t, cfg)
                method_scores.append(MethodScore(method=agent.name, score=score, details=details))
                labels_agg.update(labels or {})

            combined = combine_scores(method_scores, cfg)
            analyzed.append(TaskAnalysis(task_id=t.id, method_scores=method_scores, combined_score=combined, labels=labels_agg))
            # опционально — сразу апдейтим метки в хранилище
            if labels_agg:
                self.repo.update_task_labels(t.id, labels_agg)

        result = AnalysisResult(project_id=project_id, tasks=analyzed, created_at=datetime.utcnow(), config_used=cfg)
        self.repo.save_analysis(result)
        return result


