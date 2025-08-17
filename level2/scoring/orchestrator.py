


from __future__ import annotations
from typing import List, Dict, Any, Tuple
import math
from datetime import datetime

from level2.scoring.base import BaseScoringAgent
from level2.dto import Task, AnalysisConfig
from level2.dto import AnalysisResult

class PriorityOrchestrator:
    """
    Координатор скоринговых агентов второго уровня.
    Функции:
      - прогоняет Task через набор методов (агентов),
      - собирает результаты в единый пакет,
      - нормализует/взвешивает оценки,
      - формирует агрегированный приоритет,
      - (опционально) отдаёт снапшоты для БД/Weaviate.
    """

    def __init__(self, agents: List[BaseScoringAgent], global_weights: Dict[str, float] | None = None):
        """
        :param agents: список подключенных агентов (RICE, WSJF, KANO, MOSCOW, и т.п.).
        :param global_weights: веса методов по имени, например {"RICE":1.0, "WSJF":1.0, "KANO":0.8, ...}
        """
        self.agents: Dict[str, BaseScoringAgent] = {}
        for a in agents:
            name = getattr(a, "name", a.__class__.__name__.upper())
            a.name = name
            self.agents[name] = a

        self.global_weights = global_weights or {}

    # ====== Публичное API ======

    def analyze(self, task: Task, cfg: AnalysisConfig) -> Dict[str, Any]:
        """
        Возвращает структуру:
        {
          "by_method": {
             "RICE": {"score": float, "details": {...}, "labels": {...}},
             "WSJF": {...},
             ...
          },
          "aggregate": {
             "weighted_score": float,
             "used_methods": [...],
             "normalization": "zscore|minmax",
             "per_method_norm": {"RICE": 0.71, ...}
          },
          "snapshots": [AnalysisResult, ...]
        }
        """
        by_method: Dict[str, Dict[str, Any]] = {}
        snapshots: List[AnalysisResult] = []

        # 1) Сбор «сырых» оценок
        raw_scores: Dict[str, float] = {}
        for method in cfg.methods:
            agent = self.agents.get(method)
            if not agent:
                continue
            try:
                score, details, labels = agent.score(task, cfg)
                # защита от NaN/inf
                score = self._sanitize(score)
                by_method[method] = {"score": score, "details": details, "labels": labels}
                raw_scores[method] = score

                snapshots.append({
                    "task_id": str(task.id),
                    "method": method,
                    "score": score,
                    "labels": labels,
                    "details": details,
                    "config_used": self._extract_config_for_method(cfg, method),
                    "timestamp": datetime.utcnow().isoformat(),
                    "aggregated": False
                })
            except Exception as e:
                by_method[method] = {"error": str(e)}
                # не поднимаем исключение, чтобы один метод не валил всю аналитику

        if not raw_scores:
            return {"by_method": by_method, "aggregate": None, "snapshots": snapshots}

        # 2) Нормализация (min-max по доступным методам)
        norm_scores = self._minmax_normalize(raw_scores)

        # 3) Взвешивание (веса из конфигурации + глобальные)
        weights = self._resolve_weights(cfg, raw_scores.keys())
        weighted = {m: norm_scores[m] * weights.get(m, 1.0) for m in norm_scores}
        denom = sum(weights.get(m, 1.0) for m in norm_scores)
        weighted_score = sum(weighted.values()) / denom if denom > 0 else sum(norm_scores.values()) / len(norm_scores)

        aggregate = {
            "weighted_score": weighted_score,
            "used_methods": list(norm_scores.keys()),
            "normalization": "minmax",
            "per_method_norm": norm_scores,
            "weights": weights,
        }

        return {"by_method": by_method, "aggregate": aggregate, "snapshots": snapshots}

    def rank_tasks(self, tasks: List[Task], cfg: AnalysisConfig) -> List[Tuple[Task, Dict[str, Any]]]:
        """
        Массовый прогон и сортировка задач по агрегированному приоритету (DESC).
        Возвращает список пар (Task, analyze_result).
        """
        results: List[Tuple[Task, Dict[str, Any]]] = []
        for t in tasks:
            res = self.analyze(t, cfg)
            results.append((t, res))

        # сортируем по aggregate.weighted_score (если есть)
        results.sort(key=lambda x: (x[1].get("aggregate", {}) or {}).get("weighted_score", 0.0), reverse=True)
        return results

    # ====== Вспомогательное ======

    def _sanitize(self, x: float) -> float:
        if x is None or isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
            return 0.0
        return float(x)

    def _minmax_normalize(self, scores: Dict[str, float]) -> Dict[str, float]:
        vals = list(scores.values())
        lo, hi = min(vals), max(vals)
        if hi <= lo:
            return {k: 0.5 for k in scores}  # все равны → середина
        return {k: (v - lo) / (hi - lo) for k, v in scores.items()}

    def _resolve_weights(self, cfg: AnalysisConfig, methods: List[str]) -> Dict[str, float]:
        # 1) базовые веса из cfg.weights
        w = {m: cfg.weights.get(m, 1.0) for m in methods}
        # 2) user_overrides (если указаны)
        if cfg.user_overrides:
            for m, val in cfg.user_overrides.items():
                if m in w:
                    w[m] = float(val)
        # 3) глобальные веса из конструктора
        for m, val in self.global_weights.items():
            if m in w:
                w[m] *= float(val)
        return w

    def _extract_config_for_method(self, cfg: AnalysisConfig, method: str) -> Dict[str, Any]:
        # Встраиваем кусок конфига, релевантный методу (для трассируемости)
        if method == "RICE":
            return cfg.rice.dict()
        if method == "WSJF":
            return cfg.wsjf.dict()
        if method == "KANO":
            return cfg.kano.dict()
        if method == "MOSCOW":
            return cfg.moscow.dict()
        # для прочих методов можно вернуть пусто или общие поля
        return {}

