



from .base import BaseScoringAgent
from ..dto import Task, AnalysisConfig
from .utils import safe_float

KANO_CATEGORIES = ["must_be", "performance", "attractive", "indifferent", "reverse", "questionable"]

# Классическая таблица классификации по ответам (Functional / Dysfunctional)
# Ответы кодируются: 1=Like, 2=Must-be, 3=Neutral, 4=LiveWith, 5=Dislike
# Таблица (упрощённая):
KANO_TABLE = {
    (1,1): "questionable", (1,2): "attractive",   (1,3): "attractive",  (1,4): "attractive",  (1,5): "performance",
    (2,1): "reverse",      (2,2): "indifferent",  (2,3): "indifferent", (2,4): "indifferent", (2,5): "must_be",
    (3,1): "reverse",      (3,2): "indifferent",  (3,3): "indifferent", (3,4): "indifferent", (3,5): "must_be",
    (4,1): "reverse",      (4,2): "indifferent",  (4,3): "indifferent", (4,4): "indifferent", (4,5): "must_be",
    (5,1): "reverse",      (5,2): "reverse",      (5,3): "reverse",     (5,4): "reverse",     (5,5): "questionable",
}

def kano_class_from_votes(votes: list[tuple[int,int]]) -> dict:
    """
    votes: список пар (F, D), где F,D ∈ {1..5}
    Возвращает распределение по категориям.
    """
    counts = {k: 0 for k in KANO_CATEGORIES}
    total = 0
    for f, d in votes:
        cat = KANO_TABLE.get((int(f), int(d)), "questionable")
        counts[cat] += 1
        total += 1
    if total == 0:
        return counts
    return counts

def kano_class_major(counts: dict) -> str:
    # Мажоритарная категория по результатам опроса
    if not counts:
        return "indifferent"
    return max(counts.items(), key=lambda kv: kv[1])[0]

def kano_cs_ds(counts: dict) -> tuple[float,float]:
    """
    Индексы удовлетворенности (Berger):
      CS = (A + O) / (A + O + M + I)
      DS = (O + M) / (A + O + M + I)  (интерпретируется как «потенциал неудовлетворенности»)
    где A=Attractive, O=One-dimensional(performance), M=Must-be, I=Indifferent.
    """
    A = counts.get("attractive", 0)
    O = counts.get("performance", 0)
    M = counts.get("must_be", 0)
    I = counts.get("indifferent", 0)
    denom = A + O + M + I
    if denom == 0:
        return 0.0, 0.0
    cs = (A + O) / denom
    ds = (O + M) / denom
    return cs, ds

class KanoAgent(BaseScoringAgent):
    """
    Источники данных:
    - meta['kano_votes'] = список пар [ [F,D], ... ] (F,D ∈ 1..5)
    - при отсутствии опросных данных:
        * meta['kano_satisfaction'] (0..1), meta['kano_dissatisfaction'] (0..1)
        * или эвристика из текста/тегов (вне рамок этого файла)
    Итоговый численный score формируется так:
      score = w_cat * (alpha * CS + (1 - beta*(DS)))   (в 0.. ~1.5)
    где w_cat — вес категории (из cfg.kano), CS,DS — индексы.
    """
    name = "KANO"

    def score(self, task: Task, cfg: AnalysisConfig):
        meta = task.metadata or {}

        # 1) Попытка: явные голоса
        votes = meta.get("kano_votes")
        counts = None
        if isinstance(votes, list) and votes and isinstance(votes[0], (list, tuple)) and len(votes[0]) == 2:
            # валидация
            cleaned = []
            for f, d in votes:
                try:
                    f, d = int(f), int(d)
                    if 1 <= f <= 5 and 1 <= d <= 5:
                        cleaned.append((f, d))
                except Exception:
                    continue
            counts = kano_class_from_votes(cleaned)

        # 2) Если нет голосов — индексы из метаданных
        cs = safe_float(meta.get("kano_cs"), None)
        ds = safe_float(meta.get("kano_ds"), None)

        if counts:
            major = kano_class_major(counts)
            cs_calc, ds_calc = kano_cs_ds(counts)
            cs = cs if cs is not None else cs_calc
            ds = ds if ds is not None else ds_calc
        else:
            # Эвристика: satisfaction/dissatisfaction 0..1
            sat = safe_float(meta.get("kano_satisfaction"), 0.5)
            dis = safe_float(meta.get("kano_dissatisfaction"), 0.5)
            # При отсутствии структуры опроса — грубо оцениваем:
            major = "performance" if sat >= 0.6 and dis >= 0.4 else "attractive" if sat >= 0.7 else "indifferent"
            # Преобразуем в индексы (очень приблизительно)
            cs = sat
            ds = dis

        # веса категорий
        cat_weight_map = {
            "must_be": cfg.kano.weight_must_be,
            "performance": cfg.kano.weight_performance,
            "attractive": cfg.kano.weight_attractive,
            "indifferent": cfg.kano.weight_indifferent,
            "reverse": cfg.kano.weight_reverse,
            "questionable": 0.2,
        }
        w_cat = cat_weight_map.get(major, 0.5)

        # Итоговый численный score
        # повышаем при высоком CS; понижаем при высоком DS
        score = w_cat * (cfg.kano.alpha_cs * cs + (1.0 - cfg.kano.beta_ds * ds))

        details = {
            "category_major": major,
            "counts": counts or {},
            "CS": cs,
            "DS": ds,
            "w_cat": w_cat,
            "formula": "score = w_cat * (alpha_cs*CS + (1 - beta_ds*DS))",
            "alpha_cs": cfg.kano.alpha_cs,
            "beta_ds": cfg.kano.beta_ds,
        }
        labels = {"KANO": major}
        return score, details, labels



