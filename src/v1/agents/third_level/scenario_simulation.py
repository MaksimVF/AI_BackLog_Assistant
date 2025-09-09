


from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class ScenarioChange:
    action: str                 # 'drop' | 'delay' | 'accelerate' | 'modify'
    task_id: Optional[str] = None
    delta_value: Optional[float] = None
    delta_effort: Optional[float] = None

class ScenarioSimulationAgent:
    """
    MVP: простая симуляция "до/после" на основе value/effort.
    Примеры:
      - drop: исключить задачу из расчёта
      - delay: увеличить effort на N% (штраф за переключение контекста) и/или уменьшить value
      - accelerate: уменьшить effort (добавили ресурс), value + небольшой буст
      - modify: прямое изменение value/effort
    """

    def __init__(self,
                 delay_effort_multiplier: float = 1.10,
                 delay_value_multiplier: float = 0.95,
                 accel_effort_multiplier: float = 0.90,
                 accel_value_multiplier: float = 1.05):
        self.delay_effort_multiplier = delay_effort_multiplier
        self.delay_value_multiplier = delay_value_multiplier
        self.accel_effort_multiplier = accel_effort_multiplier
        self.accel_value_multiplier = accel_value_multiplier

    @staticmethod
    def _aggregate(tasks: List[Dict]) -> Dict:
        total_value = sum(float(t.get("value") or 0) for t in tasks)
        total_effort = sum(float(t.get("effort") or 0) for t in tasks)
        roi = (total_value / total_effort) if total_effort > 0 else 0.0
        return {"total_value": total_value, "total_effort": total_effort, "roi": roi}

    def _apply(self, tasks: List[Dict], changes: List[ScenarioChange]) -> List[Dict]:
        # индексируем задачи
        idx = {t["id"]: t.copy() for t in tasks}

        for ch in changes:
            if ch.action == "drop" and ch.task_id in idx:
                idx.pop(ch.task_id, None)

            elif ch.action == "delay" and ch.task_id in idx:
                t = idx[ch.task_id]
                t["effort"] = float(t.get("effort") or 0) * self.delay_effort_multiplier
                t["value"] = float(t.get("value") or 0) * self.delay_value_multiplier

            elif ch.action == "accelerate" and ch.task_id in idx:
                t = idx[ch.task_id]
                t["effort"] = float(t.get("effort") or 0) * self.accel_effort_multiplier
                t["value"] = float(t.get("value") or 0) * self.accel_value_multiplier

            elif ch.action == "modify" and ch.task_id in idx:
                t = idx[ch.task_id]
                if ch.delta_effort is not None:
                    t["effort"] = float(t.get("effort") or 0) + ch.delta_effort
                if ch.delta_value is not None:
                    t["value"] = float(t.get("value") or 0) + ch.delta_value

        return list(idx.values())

    def run(self, tasks: List[Dict], changes: List[ScenarioChange]) -> Dict:
        baseline = self._aggregate(tasks)
        altered_tasks = self._apply(tasks, changes)
        scenario = self._aggregate(altered_tasks)
        return {
            "baseline": baseline,
            "scenario": scenario,
            "delta": {
                "total_value": scenario["total_value"] - baseline["total_value"],
                "total_effort": scenario["total_effort"] - baseline["total_effort"],
                "roi": scenario["roi"] - baseline["roi"],
            },
            "result_tasks": altered_tasks
        }


