




from level2.dto import Task, AnalysisConfig
from level2.scoring.orchestrator import PriorityOrchestrator

from level2.scoring.rice import RiceAgent
from level2.scoring.wsjf import WSJFAgent
from level2.scoring.kano import KanoAgent
from level2.scoring.moscow import MoSCoWAgent
from level2.scoring.stack_ranking import StackRankingAgent
from level2.scoring.value_vs_effort import ValueVsEffortAgent
from level2.scoring.opportunity_scoring import OpportunityScoringAgent
from level2.strategy.purpose_alignment import PurposeAlignmentAgent
from level2.strategy.impact_mapping import ImpactMappingAgent
from level2.strategy.cost_of_delay import CostOfDelayAgent
from level2.strategy.roi import RoiAgent

# Create agents list with both traditional and strategic agents
agents = [
    RiceAgent(), WSJFAgent(), KanoAgent(), MoSCoWAgent(),
    StackRankingAgent(), ValueVsEffortAgent(), OpportunityScoringAgent(),
    PurposeAlignmentAgent(), ImpactMappingAgent(), CostOfDelayAgent(), RoiAgent()
]

# Create orchestrator with strategic agents
orchestrator = PriorityOrchestrator(agents, global_weights={"KANO": 0.8})

# Configuration with strategic methods
cfg = AnalysisConfig(
    methods=[
        "RICE","WSJF","KANO","MOSCOW","STACK_RANKING","VALUE_EFFORT","OPPORTUNITY",
        "PURPOSE_ALIGNMENT","IMPACT_MAPPING","COST_OF_DELAY","ROI"
    ],
    weights={
        "RICE":1.0,"WSJF":1.0,"KANO":0.8,"MOSCOW":0.6,
        "STACK_RANKING":0.8,"VALUE_EFFORT":1.0,"OPPORTUNITY":0.9,
        "PURPOSE_ALIGNMENT":0.7,"IMPACT_MAPPING":0.8,"COST_OF_DELAY":0.9,"ROI":1.0
    }
)

from datetime import datetime
import json

# Example tasks with strategic metadata
tasks = [
    Task(
        id="1",
        project_id="test",
        title="High ROI feature",
        created_at=datetime.now(),
        metadata={
            "expected_gain": "10000",
            "cost": "1000",
            "goals": json.dumps(["increase revenue"]),
            "project_goals": json.dumps({"increase revenue by 20%": 0.8}),
            "impact_targets": json.dumps([{"actor": "sales", "impact": 0.9}]),
            "value_per_day": "500",
            "deadline_days": "30"
        }
    ),
    Task(
        id="2",
        project_id="test",
        title="Strategic alignment task",
        created_at=datetime.now(),
        metadata={
            "expected_gain": "5000",
            "cost": "2000",
            "goals": json.dumps(["improve user retention", "expand to new markets"]),
            "project_goals": json.dumps({
                "improve user retention by 10%": 0.7,
                "expand to new markets": 0.6
            }),
            "impact_targets": json.dumps([
                {"actor": "marketing", "impact": 0.8},
                {"actor": "support", "impact": 0.7}
            ]),
            "value_per_day": "200",
            "deadline_days": "60"
        }
    )
]

# Run prioritization
for task in tasks:
    result = orchestrator.analyze(task, cfg)
    print(f"Task {task.id}: {task.title}")
    print(f"  Aggregate weighted score: {result['aggregate']['weighted_score']:.2f}")
    print(f"  Method scores:")
    for method, data in result['by_method'].items():
        print(f"    {method}: {data['score']:.2f}")
    print(f"  All labels:")
    for method, data in result['by_method'].items():
        if data['labels']:
            print(f"    {method}: {data['labels']}")
    print("  Details:")
    for method, data in result['by_method'].items():
        print(f"    {method}: {data['details']}")
    print()



