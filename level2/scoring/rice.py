


from .base import BaseScoringAgent
from ..dto import Task, AnalysisConfig
from .utils import safe_float, normalize01, extract_pert_triplet, pert_mean, clamp

class RiceAgent(BaseScoringAgent):
    """
    RICE = (Reach * Impact * Confidence) / Effort

    Дополнения:
    - Reach нормализуем к [0..1] по границам проекта (cfg.rice.reach_min/max).
    - Impact берём из якорей (tiny/low/medium/high/massive) или из метаданных value/impact.
    - Confidence ожидается 0..1 (или %).
    - Effort: поддержка PERT (effort_o/effort_m/effort_p) -> ожидание; иначе default.
    - Risk-понижение итогового score: score *= (1 - risk_penalty * risk),
      где risk = risk_prob * risk_impact (если заданы).
    """
    name = "RICE"

    def _impact_value(self, task: Task, cfg: AnalysisConfig) -> float:
        meta = task.metadata or {}
        # приоритет: явный impact_value -> якорь impact_anchor -> proxy value
        if "impact_value" in meta:
            return max(0.0, safe_float(meta.get("impact_value"), 0.0))
        anchor = (meta.get("impact_anchor") or meta.get("impact_level") or "medium").lower()
        anchors = cfg.rice.impact_anchors
        if anchor in anchors:
            return anchors[anchor]
        # fallback: использовать task.impact или метаданные value
        v = safe_float(task.impact if task.impact is not None else meta.get("value"), 1.0)
        # нормализуем к ~[0.25..3.0] (эвристика)
        return clamp(v, 0.1, 3.0)

    def _reach_value(self, task: Task, cfg: AnalysisConfig) -> float:
        meta = task.metadata or {}
        reach_raw = safe_float(task.reach if task.reach is not None else meta.get("reach"), 0.0)
        return normalize01(reach_raw, cfg.rice.reach_min, cfg.rice.reach_max)

    def _confidence_value(self, task: Task, cfg: AnalysisConfig) -> float:
        meta = task.metadata or {}
        c = task.confidence if task.confidence is not None else meta.get("confidence")
        c = safe_float(c, 0.5)
        # если в процентах
        if c > 1.0:
            c = c / 100.0
        return clamp(c, 0.0, 1.0)

    def _effort_value(self, task: Task, cfg: AnalysisConfig) -> float:
        meta = task.metadata or {}
        if cfg.rice.use_effort_pert:
            triplet = extract_pert_triplet(meta, "effort")
            if triplet:
                o, m, p = triplet
                return max(pert_mean(o, m, p), 1e-6)
        # иначе прямой effort
        eff = safe_float(task.effort if task.effort is not None else meta.get("effort"), cfg.rice.default_effort)
        return max(eff, 1e-6)

    def _risk_penalty(self, task: Task) -> float:
        meta = task.metadata or {}
        rp = clamp(safe_float(meta.get("risk_prob"), 0.0), 0.0, 1.0)
        ri = clamp(safe_float(meta.get("risk_impact"), 0.0), 0.0, 1.0)
        return clamp(rp * ri, 0.0, 1.0)

    def score(self, task: Task, cfg: AnalysisConfig):
        reach = self._reach_value(task, cfg)            # 0..1
        impact = self._impact_value(task, cfg)          # ~0.1..3.0
        confidence = self._confidence_value(task, cfg)  # 0..1
        effort = self._effort_value(task, cfg)          # >0

        base_rice = (reach * impact * confidence) / max(effort, 1e-6)

        penalty = 0.0
        if cfg.rice.risk_penalty > 0.0:
            penalty = cfg.rice.risk_penalty * self._risk_penalty(task)
        score = base_rice * (1.0 - penalty)

        details = {
            "reach_norm": reach,
            "impact": impact,
            "confidence": confidence,
            "effort": effort,
            "base_rice": base_rice,
            "risk_penalty_factor": penalty,
        }
        labels = {
            "RICE_BIN": "HIGH" if score >= 0.75 else "MEDIUM" if score >= 0.35 else "LOW"
        }
        return score, details, labels


