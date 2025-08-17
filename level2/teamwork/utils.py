

from typing import List, Dict, Any
from .dto import Vote

def normalize_vote_value(v: Vote, scheme: str = "binary"):
    """
    Преобразует Vote.value в числовую величину в зависимости от схемы.
    binary: yes=>1, no=>0, abstain=>None
    score: value ожидается числом 0..10
    rank: value — порядковый номер (1..N) -> преобразуется в score = 1/rank
    """
    val = v.value
    if scheme == "binary":
        if isinstance(val, str):
            vs = val.strip().lower()
            if vs in ("yes","y","approve","1","true"):
                return 1.0
            if vs in ("no","n","reject","0","false"):
                return 0.0
            return None  # abstain/unknown
        if isinstance(val, (int,float)):
            return float(val)
        return None
    if scheme == "score":
        try:
            return float(val)
        except Exception:
            return None
    if scheme == "rank":
        try:
            r = float(val)
            return 1.0 / r if r > 0 else None
        except Exception:
            return None
    return None

def sum_weights(votes: List[Vote], scheme: str, default_weight: float = 1.0):
    total = 0.0
    yes = 0.0
    no = 0.0
    abstain = 0.0
    breakdown = []
    for v in votes:
        w = v.weight if v.weight is not None else default_weight
        normalized = normalize_vote_value(v, scheme=scheme)
        total += w
        entry = {"voter_id": v.voter_id, "raw": v.value, "normalized": normalized, "weight": w}
        if normalized is None:
            abstain += w
            entry["bin"] = "abstain"
        elif normalized >= 0.5:
            yes += w
            entry["bin"] = "yes"
        else:
            no += w
            entry["bin"] = "no"
        breakdown.append(entry)
    return {"total": total, "yes": yes, "no": no, "abstain": abstain, "breakdown": breakdown}

