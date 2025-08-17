



from typing import Tuple, Dict, Any, List
from ..dto import VoteRequest
from ..dto import ConflictConfig
from ..scoring.utils import normalize_vote_value
import statistics

class ConflictResolutionAgent:
    name = "CONFLICT_RESOLUTION"

    def _collect_numeric_votes(self, votes: List, scheme: str = "score"):
        numeric = []
        mapping = {}
        for v in votes:
            val = normalize_vote_value(v, scheme=scheme)
            if val is not None:
                numeric.append(val)
                mapping[v.voter_id] = val
        return numeric, mapping

    def score(self, vote_req: VoteRequest, cfg: ConflictConfig = ConflictConfig()) -> Tuple[float, Dict[str, Any]]:
        """
        Оцениваем уровень конфликта:
        - используем распределение оценок от стейкхолдеров (если scheme==score/rank)
        - metric: normalized std deviation / (0..1)
        - если много участников с диаметрально противоположными оценками — повышаем severity
        Возвращаем (severity_score 0..1, details)
        """
        votes = vote_req.votes or []
        scheme = vote_req.vote_scheme or "score"

        numeric, mapping = self._collect_numeric_votes(votes, scheme=scheme)
        details = {"n_votes": len(votes)}
        if not numeric:
            # если нет числовых голосов — анализируем бинарное распределение
            yes = sum(1 for v in votes if str(v.value).lower() in ("yes","y","approve","1","true"))
            no = sum(1 for v in votes if str(v.value).lower() in ("no","n","reject","0","false"))
            total = yes + no
            if total == 0:
                return 0.0, {"reason": "no_actionable_votes"}
            # severity ~ 1 - abs(yes-no)/total  (чем ближе к 50/50 — тем выше конфликт)
            severity_raw = 1.0 - (abs(yes - no) / total)
            severity = min(1.0, severity_raw + (0.1 if len(votes) > 3 else 0.0))
            details.update({"yes": yes, "no": no, "severity_raw": severity_raw})
            level = "HIGH" if severity >= cfg.severity_threshold else "MEDIUM" if severity >= cfg.severity_threshold*0.6 else "LOW"
            return float(severity), {"level": level, **details}

        # если есть числовые оценки — используем стандартное отклонение относительно диапазона
        try:
            std = statistics.pstdev(numeric)
            mean = statistics.mean(numeric)
        except Exception:
            return 0.0, {"reason": "stat_error"}

        # нормализуем std: предположим оценки в 0..1 (если нет — попытаемся нормализовать)
        max_possible = max(numeric) if numeric else 1.0
        if max_possible <= 1e-6:
            normalized_std = std
        else:
            normalized_std = std / max_possible

        # базовый severity
        severity = min(1.0, normalized_std + (cfg.multi_stakeholder_penalty if len(numeric) > 3 else 0.0))
        level = "HIGH" if severity >= cfg.severity_threshold else "MEDIUM" if severity >= cfg.severity_threshold*0.6 else "LOW"
        details.update({"mean": mean, "std": std, "normalized_std": normalized_std, "mapping": mapping})
        return float(severity), {"level": level, **details}



