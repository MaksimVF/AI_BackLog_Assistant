





from typing import List, Dict, Any
from collections import deque

# TODO: Import SentenceTransformer when available
# from sentence_transformers import SentenceTransformer, util

class ContextMemoryAgent:
    """
    ContextMemoryAgent: Долговременное хранение контекстов.

    Долговременное хранение контекстов, фрагментов и связей, созданных другими подагентами;
    выбор релевантной информации из памяти при новых задачах (рефлексия, категоризация, планирование и пр.);
    управление памятью — обновление, удаление устаревших или малозначимых контекстов.
    """

    def __init__(self, max_memory: int = 1000, model_name: str = "all-MiniLM-L6-v2"):
        self.memory = deque(maxlen=max_memory)
        # TODO: Initialize SentenceTransformer when available
        # self.model = SentenceTransformer(model_name)

    def add_context(self, context: Dict[str, Any]):
        """
        Добавляет новый контекст в память. Контекст должен содержать ключ 'text'.

        Args:
            context: Контекст для добавления
        """
        # TODO: Add embedding when SentenceTransformer is available
        # context["embedding"] = self.model.encode(context["text"], convert_to_tensor=True)
        self.memory.append(context)

    def retrieve_relevant(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Возвращает top_k наиболее релевантных контекстов по смыслу.

        Args:
            query: Запрос для поиска
            top_k: Количество результатов

        Returns:
            Список релевантных контекстов
        """
        # TODO: Implement semantic search when SentenceTransformer is available
        # query_emb = self.model.encode(query, convert_to_tensor=True)
        # scored = []
        #
        # for item in self.memory:
        #     sim = util.pytorch_cos_sim(query_emb, item["embedding"])[0][0].item()
        #     scored.append((sim, item))
        #
        # scored.sort(reverse=True, key=lambda x: x[0])
        # return [item for _, item in scored[:top_k]]

        # For now, use simple keyword matching
        query_words = set(query.lower().split())
        scored = []

        for item in self.memory:
            text = item.get("text", "").lower()
            common_words = len(query_words.intersection(text.split()))
            score = common_words / max(len(query_words), 1)
            scored.append((score, item))

        scored.sort(reverse=True, key=lambda x: x[0])
        return [item for _, item in scored[:top_k]]

    def clear_memory(self):
        """Очищает память."""
        self.memory.clear()





