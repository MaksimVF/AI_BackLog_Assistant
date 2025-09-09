

from typing import Dict, Any, List

class SemanticConsistencyChecker:
    """
    Проверяет семантическую согласованность документа:
    - выявляет логические противоречия,
    - отмечает пропущенные обязательные элементы,
    - оценивает полноту содержания.
    """

    def __init__(self, required_sections: List[str] = None):
        # Стандартный набор обязательных секций для юридических документов
        self.required_sections = required_sections or [
            "title",
            "parties",
            "effective_date",
            "terms",
            "obligations",
            "termination",
            "signatures"
        ]

    def analyze(self, document_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        document_structure — словарь с ключами-секциями документа и их содержимым
        """
        missing_sections = [sec for sec in self.required_sections if sec not in document_structure]

        # Простейшая проверка логики - можно расширить интеграцией с NLP-моделями
        contradictions = self._check_basic_contradictions(document_structure)

        result = {
            "missing_sections": missing_sections,
            "contradictions_found": contradictions,
            "is_complete": len(missing_sections) == 0 and len(contradictions) == 0,
            "recommendation": self._generate_recommendation(missing_sections, contradictions)
        }
        return result

    def _check_basic_contradictions(self, document_structure: Dict[str, Any]) -> List[str]:
        """
        Базовая проверка логических противоречий в документе
        """
        contradictions = []

        # Пример: проверка противоречий в датах
        if "effective_date" in document_structure and "termination_date" in document_structure:
            try:
                effective = document_structure["effective_date"]
                termination = document_structure["termination_date"]

                if effective > termination:
                    contradictions.append(
                        "Дата начала действия договора позже даты его прекращения"
                    )
            except (TypeError, ValueError):
                # Если даты не в правильном формате
                contradictions.append("Формат дат некорректен")

        # Пример: проверка противоречий в обязательствах
        if "obligations" in document_structure and isinstance(document_structure["obligations"], dict):
            obligations = document_structure["obligations"]
            for party, obligation_text in obligations.items():
                if "не обязан" in obligation_text.lower() and "обязуется" in obligation_text.lower():
                    contradictions.append(
                        f"Противоречие в обязательствах для {party}: одновременно указано 'обязуется' и 'не обязан'"
                    )

        return contradictions

    def _generate_recommendation(self, missing_sections: List[str], contradictions: List[str]) -> str:
        """
        Генерирует рекомендации на основе найденных проблем
        """
        if missing_sections and contradictions:
            return "Документ требует существенной доработки: отсутствуют обязательные разделы и обнаружены логические противоречия."
        elif missing_sections:
            return f"Документ неполный. Отсутствуют разделы: {', '.join(missing_sections)}"
        elif contradictions:
            return "В документе обнаружены логические противоречия. Требуется ревизия."
        else:
            return "Документ семантически корректен."

