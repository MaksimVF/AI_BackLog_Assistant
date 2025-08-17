


from typing import Tuple, Dict, Any
from ..dto import VoteRequest, VoteResult, VotingConfig
from ..scoring.utils import sum_weights

class VotingConsensusAgent:
    name = "VOTING_CONSENSUS"

    def score(self, vote_req: VoteRequest, cfg: VotingConfig = VotingConfig()) -> Tuple[VoteResult, Dict, Any]:
        """
        Проводит агрегирование голосов и выводит результат консенсуса.
        Возвращает (VoteResult, internals_for_audit)
        """
        votes = vote_req.votes or []
        scheme = vote_req.vote_scheme or "binary"
        sums = sum_weights(votes, scheme, default_weight=cfg.default_weight)

        total = sums["total"]
        yes = sums["yes"]
        no = sums["no"]
        abstain = sums["abstain"]

        quorum = (total >= cfg.quorum_ratio * max(1.0, len(votes)*cfg.default_weight))
        consensus = False
        decision = None

        # расчет доли "за" среди принявших участие (exclude abstain)
        participants_weight = total - abstain if total - abstain > 0 else total
        yes_ratio = (yes / participants_weight) if participants_weight > 0 else 0.0
        no_ratio = (no / participants_weight) if participants_weight > 0 else 0.0

        if quorum and yes_ratio >= cfg.consensus_threshold and yes_ratio > no_ratio:
            consensus = True
            decision = "approve"
        elif quorum and no_ratio >= cfg.consensus_threshold and no_ratio > yes_ratio:
            consensus = True
            decision = "reject"
        else:
            consensus = False
            decision = "no_consensus"

        result = VoteResult(
            task_id=vote_req.task_id,
            quorum=quorum,
            total_weight=total,
            yes_weight=yes,
            no_weight=no,
            abstain_weight=abstain,
            consensus=consensus,
            decision=decision,
            breakdown={"participants": sums["breakdown"], "yes_ratio": yes_ratio, "no_ratio": no_ratio}
        )
        internals = {"raw": sums}
        return result, internals


