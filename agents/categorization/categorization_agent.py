


from .document_classifier_agent import DocumentClassifierAgent
from .domain_classifier_agent import DomainClassifierAgent
from .semantic_tagging_agent import SemanticTaggingAgent
from .similarity_matcher_agent import SimilarityMatcherAgent
from .document_group_assigner_agent import DocumentGroupAssignerAgent

class CategorizationAgent:
    """
    CategorizationAgent: Комплексная категоризация документов.

    Объединяет все подагенты для полной категоризации документа:
    - Определение типа документа
    - Классификация предметной области
    - Семантическая разметка
    - Поиск похожих документов
    - Назначение группы/кластера
    """

    def __init__(self):
        self.document_classifier = DocumentClassifierAgent()
        self.domain_classifier = DomainClassifierAgent()
        self.semantic_tagger = SemanticTaggingAgent()
        self.similarity_matcher = SimilarityMatcherAgent()
        self.group_assigner = DocumentGroupAssignerAgent()

    def categorize_document(self, document_text: str, metadata: dict = None) -> dict:
        """
        Perform comprehensive categorization of the document.

        Args:
            document_text: The document text to categorize
            metadata: Optional metadata about the document

        Returns:
            A dictionary containing all categorization results
        """
        # Classify document type
        document_type = self.document_classifier.classify(document_text)

        # Classify domain
        domain = self.domain_classifier.classify(document_text)

        # Extract semantic tags
        tags = self.semantic_tagger.extract_tags(document_text)

        # Find similar documents
        similar_docs = self.similarity_matcher.find_similar_documents(document_text)

        # Assign document group
        group = self.group_assigner.assign_group(document_text)

        return {
            "document_type": document_type,
            "domain": domain,
            "semantic_tags": tags,
            "similar_documents": similar_docs,
            "group": group
        }



