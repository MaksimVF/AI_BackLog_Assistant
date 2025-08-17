


def safe_float(v, default=0.0):
    try:
        return float(v)
    except Exception:
        return default

def clamp(v, min_v, max_v):
    return max(min_v, min(max_v, v))

def sum_weights(votes, field="weight"):
    """Sum weights from a list of votes."""
    return sum(getattr(v, field, 1.0) for v in votes)

def normalize_vote_value(value):
    """Normalize vote value to a standard scale."""
    if isinstance(value, str):
        value = value.lower()
        if value in ["yes", "agree", "approve"]:
            return 1.0
        elif value in ["no", "disagree", "reject"]:
            return -1.0
        else:
            return 0.0
    return float(value)


