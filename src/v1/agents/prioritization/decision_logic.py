

class DecisionLogic:
    def __init__(self, factors):
        self.factors = factors

    def make_decision(self):
        """
        На основе анализа факторов принимает решение:
        - 'recommend' — рекомендовать выполнение
        - 'postpone' — отложить
        - 'reject' — отклонить
        Логика упрощённая, может быть расширена.
        """
        priority = self.factors.get("priority", 0)
        effort = self.factors.get("effort", 1)
        criticality = self.factors.get("criticality", 0)
        risk = self.factors.get("risk", 0)

        # Calculate decision score - higher threshold for recommendation
        score = (priority * criticality) / max(effort, 1)

        # Adjust thresholds to be more selective
        if score > 100 and criticality >= 7:
            return "recommend"
        elif score > 50 or criticality >= 5:
            return "postpone"
        else:
            return "reject"

