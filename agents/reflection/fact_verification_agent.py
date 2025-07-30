


from core.llm_client import chat_completion
from tools.utils.text_splitter import chunk_text

class FactVerificationAgent:
    """
    Проверяет фактическую точность утверждений в тексте с использованием LLM.
    """

    def __init__(self):
        self.name = "FactVerificationAgent"

    def verify_facts(self, text: str) -> dict:
        """
        Проверяет текст на наличие фактических ошибок.
        """
        chunks = chunk_text(text)
        results = []

        for chunk in chunks:
            prompt = (
                "Проверь следующие утверждения на наличие фактических ошибок. "
                "Если есть ошибки — опиши. Если всё корректно — ответь 'Факты подтверждаются.'\n\n"
                f"{chunk}"
            )
            response = chat_completion(prompt)
            results.append(response)

        return {"verification_results": results}


