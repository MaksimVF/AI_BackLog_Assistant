

class RecommendationReporter:
    def __init__(self, decision, details=None):
        self.decision = decision
        self.details = details or {}

    def generate_report(self):
        """
        Возвращает структурированный отчёт с рекомендацией и пояснениями.
        """
        explanations = {
            "recommend": "Задача приоритетна и критична, рекомендуется выполнить в ближайшее время.",
            "postpone": "Задача важна, но может быть отложена без серьёзных последствий.",
            "reject": "Задача имеет низкий приоритет или критичность, рекомендуется отклонить."
        }
        report = {
            "decision": self.decision,
            "explanation": explanations.get(self.decision, "Нет данных для объяснения."),
            "details": self.details
        }
        return report

