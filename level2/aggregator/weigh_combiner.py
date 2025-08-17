


from typing import List
from ..dto import MethodScore, AnalysisConfig

def combine_scores(method_scores: List[MethodScore], cfg: AnalysisConfig) -> float:
    num = 0.0
    den = 0.0
    for ms in method_scores:
        w = cfg.weights.get(ms.method.upper(), 1.0)
        num += w * ms.score
        den += w
    return num / den if den else 0.0


