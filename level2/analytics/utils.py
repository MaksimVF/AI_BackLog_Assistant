





from typing import List, Tuple
import math

def linear_regression(xs: List[float], ys: List[float]) -> Tuple[float, float]:
    """
    Простая линейная регрессия (y = a + b*x).
    Возвращает (a, b). При недостатке данных возвращает (mean_y, 0.0).
    """
    n = len(xs)
    if n == 0:
        return 0.0, 0.0
    if n == 1:
        return ys[0], 0.0
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = 0.0
    den = 0.0
    for x, y in zip(xs, ys):
        num += (x - mean_x) * (y - mean_y)
        den += (x - mean_x) ** 2
    if abs(den) < 1e-9:
        return mean_y, 0.0
    b = num / den
    a = mean_y - b * mean_x
    return a, b

def moving_average(values: List[float], window: int) -> List[float]:
    if window <= 0:
        return values[:]
    res = []
    for i in range(len(values)):
        start = max(0, i - window + 1)
        window_vals = values[start:i+1]
        res.append(sum(window_vals) / len(window_vals))
    return res

def safe_float(x, default=0.0):
    try:
        if x is None:
            return default
        return float(x)
    except Exception:
        return default

def pct_change(prev, curr):
    if prev == 0:
        return None
    return (curr - prev) / prev





