


from agents.third_level.scenario_simulation import ScenarioSimulationAgent, ScenarioChange
from app_third_level import ScenarioChangeIn

# Test data
tasks = [
    {"id": "task_123", "title": "Task 1", "value": 10.0, "effort": 3.0},
    {"id": "task_456", "title": "Task 2", "value": 6.0, "effort": 4.0},
    {"id": "task_789", "title": "Task 3", "value": 2.0, "effort": 5.0}
]

# Test the conversion
change_in = ScenarioChangeIn(action="drop", task_id="task_123")
print("ScenarioChangeIn:", change_in.dict())

change = ScenarioChange(**change_in.dict())
print("ScenarioChange:", change)

changes = [
    ScenarioChange(action="drop", task_id="task_123"),
    ScenarioChange(action="accelerate", task_id="task_456", delta_value=2.0, delta_effort=-1.0)
]

# Run the agent
agent = ScenarioSimulationAgent()
result = agent.run(tasks, changes)

print("Baseline:", result["baseline"])
print("Scenario:", result["scenario"])
print("Delta:", result["delta"])
print("Result tasks:", result["result_tasks"])


