


class DecisionAgent:
    def __init__(self, prioritization_agent, recommendation_reporter):
        self.prioritization_agent = prioritization_agent
        self.recommendation_reporter = recommendation_reporter

    def make_decision(self, task_data):
        # Получаем приоритет и другие параметры от агента приоритизации
        priority_data = self.prioritization_agent.evaluate(task_data)

        # На основе приоритета и дополнительных параметров принимаем решение
        decision = self._decide(priority_data)

        # Формируем отчёт с рекомендацией
        report = self.recommendation_reporter(decision, details=priority_data).generate_report()

        return report

    def _decide(self, priority_data):
        score = priority_data.get("score", 0)
        criticality = priority_data.get("criticality", 0)

        # Пример правил принятия решения
        if score >= 7 and criticality >= 7:
            return "recommend"
        elif 4 <= score < 7:
            return "postpone"
        else:
            return "reject"


