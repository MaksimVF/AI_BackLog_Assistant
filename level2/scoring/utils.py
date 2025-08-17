

from typing import Optional, Tuple

def safe_float(x, default: float = 0.0) -> float:
    try:
        if x is None:
            return default
        return float(x)
    except Exception:
        return default

def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))

def normalize01(x: float, lo: float, hi: float) -> float:
    if hi <= lo:
        return 0.0
    return clamp((x - lo) / (hi - lo), 0.0, 1.0)

def pert_mean(o: float, m: float, p: float) -> float:
    # PERT-ожидание
    return (o + 4*m + p) / 6.0

def pert_std(o: float, m: float, p: float) -> float:
    # аппрокс. стандартное отклонение по PERT
    return (p - o) / 6.0

def extract_pert_triplet(meta: dict, prefix: str) -> Optional[Tuple[float, float, float]]:
    # ожидает meta[f"{prefix}_o|m|p"]
    try:
        o = safe_float(meta.get(f"{prefix}_o"))
        m = safe_float(meta.get(f"{prefix}_m"))
        p = safe_float(meta.get(f"{prefix}_p"))
        if (o > 0 or m > 0 or p > 0):
            return o, m, p
        return None
    except Exception:
        return None

