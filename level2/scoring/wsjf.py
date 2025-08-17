


from .base import BaseScoringAgent
from ..dto import Task, AnalysisConfig
from .utils import safe_float, clamp, normalize01, extract_pert_triplet, pert_mean

class WSJFAgent(BaseScoringAgent):
    """
    WSJF = (BV + TC + RR/OE) / JobSize

    Где:
    - BV (Business Value), TC (Time Criticality), RR/OE (Risk Reduction/Opportunity Enablement)
      оцениваются в отн. шкале (обычно 1..10). Здесь допускаем:
        * явные meta: bv, tc, rr_oe   (могут быть в 0..100 → нормализуем к 1..10)
        * либо извлекаем прокси из task.metadata (например, "revenue_impact", "deadline_days", "risk_reduction_flag")
    - JobSize ← из effort (PERT при наличии).
    - Поддерживаются веса компонент (cfg.wsjf.weight_*).
    """
    name = "WSJF"

    def _scale_to_band(self, x: float, lo: float, hi: float, band_lo: float, band_hi: float) -> float:
        # линейная нормализация в заданный диапазон (например, 1..10)
        n = normalize01(x, lo, hi)
        return band_lo + n * (band_hi - band_lo)

    def _bv(self, task: Task, cfg: AnalysisConfig) -> float:
        meta = task.metadata or {}
        bv = meta.get("bv")
        if bv is not None:
            bv = safe_float(bv, 0.0)
            # если похоже на % или 0..100 — нормализуем в 1..10
            if bv > cfg.wsjf.max_score:
                return clamp(self._scale_to_band(bv, 0.0, 100.0, cfg.wsjf.min_score, cfg.wsjf.max_score),
                             cfg.wsjf.min_score, cfg.wsjf.max_score)
            return clamp(bv, cfg.wsjf.min_score, cfg.wsjf.max_score)
        # proxy: выручка/ценность
        value = safe_float(meta.get("value", task.impact if task.impact is not None else 1.0), 1.0)
        # приведём value (0..3) к 1..10
        return clamp(self._scale_to_band(value, 0.0, 3.0, cfg.wsjf.min_score, cfg.wsjf.max_score),
                     cfg.wsjf.min_score, cfg.wsjf.max_score)

    def _tc(self, task: Task, cfg: AnalysisConfig) -> float:
        meta = task.metadata or {}
        tc = meta.get("tc")
        if tc is not None:
            tc = safe_float(tc, 0.0)
            if tc > cfg.wsjf.max_score:
                return clamp(self._scale_to_band(tc, 0.0, 100.0, cfg.wsjf.min_score, cfg.wsjf.max_score),
                             cfg.wsjf.min_score, cfg.wsjf.max_score)
            return clamp(tc, cfg.wsjf.min_score, cfg.wsjf.max_score)
        # proxy: дедлайн — чем ближе, тем выше TC
        deadline_days = safe_float(meta.get("deadline_days"), 9999.0)
        if deadline_days >= 9999.0:
            # без дедлайна — средняя критичность
            return (cfg.wsjf.min_score + cfg.wsjf.max_score) / 2.0
        # обратная зависимость: 0 дней → 10; 60+ дней → ~1
        tc_raw = max(0.0, 60.0 - deadline_days)
        return clamp(self._scale_to_band(tc_raw, 0.0, 60.0, cfg.wsjf.min_score, cfg.wsjf.max_score),
                     cfg.wsjf.min_score, cfg.wsjf.max_score)

    def _rr_oe(self, task: Task, cfg: AnalysisConfig) -> float:
        meta = task.metadata or {}
        rr = meta.get("rr_oe")
        if rr is not None:
            rr = safe_float(rr, 0.0)
            if rr > cfg.wsjf.max_score:
                return clamp(self._scale_to_band(rr, 0.0, 100.0, cfg.wsjf.min_score, cfg.wsjf.max_score),
                             cfg.wsjf.min_score, cfg.wsjf.max_score)
            return clamp(rr, cfg.wsjf.min_score, cfg.wsjf.max_score)
        # proxy: снижение риска / открытие возможности
        risk_reduction_flag = safe_float(meta.get("risk_reduction_flag"), 0.0)  # 0..1
        opp_enable_flag = safe_float(meta.get("opportunity_flag"), 0.0)         # 0..1
        rr_raw = clamp(risk_reduction_flag * 0.6 + opp_enable_flag * 0.4, 0.0, 1.0)
        return clamp(self._scale_to_band(rr_raw, 0.0, 1.0, cfg.wsjf.min_score, cfg.wsjf.max_score),
                     cfg.wsjf.min_score, cfg.wsjf.max_score)

    def _job_size(self, task: Task, cfg: AnalysisConfig) -> float:
        meta = task.metadata or {}
        if cfg.wsjf.use_effort_pert:
            triplet = extract_pert_triplet(meta, "effort")
            if triplet:
                o, m, p = triplet
                return max(pert_mean(o, m, p), 1e-6)
        eff = safe_float(task.effort if task.effort is not None else meta.get("effort"), cfg.wsjf.default_effort)
        return max(eff, 1e-6)

    def score(self, task: Task, cfg: AnalysisConfig):
        bv = self._bv(task, cfg)
        tc = self._tc(task, cfg)
        rr = self._rr_oe(task, cfg)
        job_size = self._job_size(task, cfg)

        # веса компонент
        bv_w = cfg.wsjf.weight_bv * bv
        tc_w = cfg.wsjf.weight_tc * tc
        rr_w = cfg.wsjf.weight_rr_oe * rr

        numerator = bv_w + tc_w + rr_w
        score = numerator / job_size

        details = {
            "BV": bv, "TC": tc, "RR_OE": rr,
            "BV_weighted": bv_w, "TC_weighted": tc_w, "RR_OE_weighted": rr_w,
            "job_size": job_size, "numerator": numerator
        }
        labels = {"WSJF_BIN": "HIGH" if score >= 1.5 else "MEDIUM" if score >= 0.7 else "LOW"}
        return score, details, labels


