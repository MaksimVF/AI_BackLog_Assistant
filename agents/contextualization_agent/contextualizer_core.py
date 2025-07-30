





from .knowledge_graph_agent import KnowledgeGraphAgent
from .document_relinker_agent import DocumentRelinkerAgent
from .context_memory_agent import ContextMemoryAgent
from .reference_matcher_agent import ReferenceMatcherAgent

from typing import List, Dict, Any

class ContextualizerCore:
    """
    ContextualizerCore: Центральный координатор контекстуализации.

    Координирует работу всех подагентов контекстуализации:
    - KnowledgeGraphAgent
    - DocumentRelinkerAgent
    - ContextMemoryAgent
    - ReferenceMatcherAgent

    Формирует полное описание документа в терминах структуры, блоков и связей,
    сохраняет всё в долговременную память,
    обеспечивает доступ к релевантной информации другим агентам.
    """

    def __init__(self):
        self.knowledge_graph_agent = KnowledgeGraphAgent()
        self.document_relinker = DocumentRelinkerAgent()
        self.context_memory = ContextMemoryAgent()
        self.reference_matcher = ReferenceMatcherAgent()

    def process_document(self, document_text: str) -> Dict[str, Any]:
        """
        Главный метод: обрабатывает документ, строит граф знаний, связывает блоки,
        ищет референсы и сохраняет в память.

        Args:
            document_text: Текст документа для обработки

        Returns:
            Контекст документа с полной информацией
        """
        # Split document into chunks (simple implementation)
        chunks = [paragraph.strip() for paragraph in document_text.split('\n\n') if paragraph.strip()]

        # Build knowledge graph
        knowledge_graph = self.knowledge_graph_agent.build_graph(document_text)

        # Find references in knowledge base
        references = self.reference_matcher.match_references(chunks)

        # Link document blocks
        blocks = [{"source": "document", "text": chunk} for chunk in chunks]
        clusters = self.document_relinker.link_documents(blocks)

        # Create context object
        context = {
            "text": document_text,
            "chunks": chunks,
            "knowledge_graph": knowledge_graph,
            "references": references,
            "clusters": clusters,
        }

        # Store in memory
        self.context_memory.add_context(context)

        return context

    def get_context_for_query(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Возвращает релевантный контекст по смысловому запросу.

        Args:
            query: Запрос для поиска
            top_k: Количество результатов

        Returns:
            Список релевантных контекстов
        """
        return self.context_memory.retrieve_relevant(query, top_k=top_k)

    def clear_context_memory(self):
        """Очищает память контекстов."""
        self.context_memory.clear_memory()






