



from level2.dto import Task, AnalysisConfig
from level2.scoring.orchestrator import PriorityOrchestrator

from level2.scoring.rice import RiceAgent
from level2.scoring.wsjf import WSJFAgent
from level2.scoring.kano import KanoAgent
from level2.scoring.moscow import MoSCoWAgent
from level2.scoring.stack_ranking import StackRankingAgent
from level2.scoring.value_vs_effort import ValueVsEffortAgent
from level2.scoring.opportunity_scoring import OpportunityScoringAgent

agents = [
    RiceAgent(), WSJFAgent(), KanoAgent(), MoSCoWAgent(),
    StackRankingAgent(), ValueVsEffortAgent(), OpportunityScoringAgent()
]

orchestrator = PriorityOrchestrator(agents, global_weights={"KANO": 0.8})

cfg = AnalysisConfig(
    methods=["RICE","WSJF","KANO","MOSCOW","STACK_RANKING","VALUE_EFFORT","OPPORTUNITY"],
    weights={"RICE":1.0,"WSJF":1.0,"KANO":0.8,"MOSCOW":0.6,"STACK_RANKING":0.8,"VALUE_EFFORT":1.0,"OPPORTUNITY":0.9}
)

from datetime import datetime

tasks = [
    Task(id="A", project_id="test", title="Realtime analytics", reach=8000, impact=2.0, confidence=0.8, effort=5,
         created_at=datetime.now(),
         metadata={"bv":"9","tc":"6","rr_oe":"3","importance":"8","satisfaction":"4","value":"7","votes":"70,80,90"}),
    Task(id="B", project_id="test", title="User profile page", reach=1200, impact=1.0, confidence=0.9, effort=2,
         created_at=datetime.now(),
         metadata={"bv":"5","tc":"3","rr_oe":"2","importance":"6","satisfaction":"5","value":"6","votes":"60,70,65"}),
    Task(id="C", project_id="test", title="API documentation", reach=500, impact=0.5, confidence=0.7, effort=1,
         created_at=datetime.now(),
         metadata={"bv":"3","tc":"2","rr_oe":"1","importance":"4","satisfaction":"3","value":"5","votes":"50,55,60"})
]

# Run analysis
for task in tasks:
    result = orchestrator.analyze(task, cfg)
    print(f"Task {task.id}: {task.title}")
    print(f"  Weighted score: {result['aggregate']['weighted_score']:.2f}")
    for method, data in result['by_method'].items():
        if 'error' in data:
            print(f"  {method}: ERROR - {data['error']}")
        else:
            print(f"  {method}: {data['score']:.2f} ({data['labels']})")
    print()

# Rank tasks
ranked = orchestrator.rank_tasks(tasks, cfg)
print("Ranked tasks:")
for i, (task, result) in enumerate(ranked, 1):
    score = result['aggregate']['weighted_score']
    print(f"{i}. {task.title} - {score:.2f}")


