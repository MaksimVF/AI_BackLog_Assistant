









from typing import Tuple, Dict, Any, List, Callable
from level2.dto import Task
from ..dto import ForensicConfig
from ..utils import safe_float, pct_change
import collections

class ForensicAnalysisAgent:
    name = "FORENSIC_ANALYSIS"

    def score(self, tasks_history: List[Task], cfg: ForensicConfig, repo_fetcher: Callable[[str], Task] = None) -> Tuple[float, Dict[str, Any], Dict[str, str]]:
        """
        tasks_history — список задач/итераций (прошлые задачи, связанные с проектом)
        Возвращает summary score (0..1) — степень проблемности, details и labels.
        """
        if not tasks_history:
            return 0.0, {"reason": "no_history"}, {"FORENSIC": "EMPTY"}

        # 1) Анализ недооценки: сравним estimate vs actual (metadata: est_effort / actual_effort)
        under_estimates = 0
        total = 0
        under_by = []
        blockers = collections.Counter()
        resource_issues = 0
        delays = []
        for t in tasks_history:
            meta = t.metadata or {}
            est = safe_float(meta.get("est_effort"), None)
            actual = safe_float(meta.get("actual_effort"), None)
            if est is not None and actual is not None:
                total += 1
                if actual > est * (1.0 + cfg.delay_threshold_ratio):
                    under_estimates += 1
                    under_by.append((t.id, actual/est if est>0 else None))
            # blockers
            b = meta.get("blockers") or []
            for bl in b:
                blockers[bl] += 1
            if meta.get("resource_issue"):
                resource_issues += 1
            # delays measure (days)
            delay_days = safe_float(meta.get("delay_days"), 0.0)
            if delay_days > 0:
                delays.append(delay_days)

        # 2) recurrent causes
        common_blockers = blockers.most_common(5)
        recurrence_score = min(1.0, sum((cnt for _,cnt in common_blockers)) / max(1, len(tasks_history)))

        underestimate_ratio = (under_estimates / total) if total else 0.0
        avg_delay = (sum(delays) / len(delays)) if delays else 0.0

        # 3) forensic "severity"
        severity = min(1.0, 0.6 * underestimate_ratio + 0.2 * recurrence_score + 0.2 * (resource_issues / max(1, len(tasks_history))))

        details = {
            "records": len(tasks_history),
            "under_estimates": under_estimates,
            "total_est_records": total,
            "under_by_examples": under_by[:5],
            "common_blockers": common_blockers,
            "resource_issues": resource_issues,
            "avg_delay_days": avg_delay
        }

        recommendations = []
        if underestimate_ratio > 0.2:
            recommendations.append("Review estimation process; enforce PERT or planning poker for similar tasks.")
        if recurrence_score > 0.1:
            recommendations.append("Investigate top blockers and create dedicated remediation tasks.")
        if resource_issues / max(1, len(tasks_history)) > 0.1:
            recommendations.append("Address resource allocation (hiring/redistribute).")

        details["recommendations"] = recommendations
        label = "CRITICAL" if severity >= 0.7 else "HIGH" if severity >= 0.4 else "OK"
        return float(severity), details, {"FORENSIC_LEVEL": label}









