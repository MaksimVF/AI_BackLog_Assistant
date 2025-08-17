



from typing import Tuple, Dict, Any

from ..dto import StakeholderAlignmentConfig
from level2.dto import Task

from ..scoring.utils import safe_float, clamp

class StakeholderAlignmentAgent:
    name = "STAKEHOLDER_ALIGNMENT"

    def score(self, task: Task, cfg: StakeholderAlignmentConfig, project_stakeholders: Dict[str, Dict[str, Any]] = None) -> Tuple[float, Dict[str, Any]]:
        """
        project_stakeholders: {id: {"weight":0.5, "priorities": {"areaA":0.8,...}}}
        task.metadata may include "priority_vector": {stakeholder_id: priority_value}
        """
        meta = task.metadata or {}
        task_vec = meta.get("priority_vector") or {}  # {stakeholder_id: priority 0..1}
        if not project_stakeholders:
            # если нет профиля стейкхолдеров, рассматриваем одностороннее совпадение с average
            if not task_vec:
                return 0.0, {"reason": "no_data"}
            avg = sum(float(v) for v in task_vec.values()) / max(len(task_vec),1)
            return float(clamp(avg, 0.0, 1.0)), {"method": "task_avg", "avg": avg}

        # сравниваем task_vec с profile: взвешенное скалярное совпадение
        numer = 0.0
        denom = 0.0
        details = {"per_stakeholder": {}}
        for sid, profile in project_stakeholders.items():
            weight = safe_float(profile.get("weight"), 1.0)
            stakeholder_priority = safe_float(task_vec.get(sid), 0.0)
            numer += weight * stakeholder_priority
            denom += weight
            details["per_stakeholder"][sid] = {"weight": weight, "task_priority": stakeholder_priority}

        score = (numer / denom) if denom > 0 else 0.0
        aligned = "aligned" if score >= cfg.aligned_threshold else "misaligned"
        labels = {"STAKEHOLDER_ALIGNMENT": aligned}
        return float(clamp(score, 0.0, 1.0)), {"score": score, "details": details}, labels




