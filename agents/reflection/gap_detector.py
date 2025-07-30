
from typing import Dict, Any, List

class GapDetector:
    """
    Обнаруживает отсутствующие ключевые поля или фрагменты в структурированных данных.
    """

    def __init__(self):
        # Определим список обязательных ключевых полей (можно расширять динамически по типу документа)
        self.required_fields = [
            "document_title",
            "document_type",
            "date_created",
            "counterparty_name",
            "signatory",
            "jurisdiction"
        ]

    def detect_gaps(self, structured_data: Dict[str, Any]) -> List[str]:
        """
        Возвращает список отсутствующих полей, необходимых для юридического анализа.
        """
        missing = []
        for field in self.required_fields:
            value = structured_data.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                missing.append(field)
        return missing

    def evaluate(self, structured_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Анализирует данные и возвращает статус полноты.
        """
        missing_fields = self.detect_gaps(structured_data)
        return {
            "missing_fields_found": bool(missing_fields),
            "missing_fields": missing_fields,
            "recommendation": "Необходимо дополнить документ" if missing_fields else "OK"
        }
