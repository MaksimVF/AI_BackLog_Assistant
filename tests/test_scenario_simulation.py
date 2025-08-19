


import pytest
from agents.third_level.scenario_simulation import ScenarioSimulationAgent, ScenarioChange

def test_drop_scenario():
    agent = ScenarioSimulationAgent()
    tasks = [{"id": 1, "value": 10, "effort": 5}, {"id": 2, "value": 20, "effort": 10}]
    result = agent.run(tasks, [ScenarioChange(action="drop", task_id=1)])
    assert result["scenario"]["total_value"] == 20
    assert result["scenario"]["total_effort"] == 10

def test_accelerate_scenario():
    agent = ScenarioSimulationAgent(accel_value_multiplier=1.1)
    tasks = [{"id": 1, "value": 10, "effort": 5}]
    result = agent.run(tasks, [ScenarioChange(action="accelerate", task_id=1)])
    assert result["scenario"]["total_value"] > 10
    assert result["scenario"]["total_effort"] < 5


