

from .document_classifier_agent import DocumentClassifierAgent
from .domain_classifier_agent import DomainClassifierAgent
from .taxonomy_mapper_agent import TaxonomyMapperAgent
from .tagging_agent import TaggingAgent

class CategorizationAgent:
    """
    CategorizationAgent: Общее описание

    Цель:
    На основании текста (и метаданных) от других агентов:
    - определить категорию (вид документа / сущности),
    - связать с иерархией (справочники, налоговые коды, классификаторы),
    - подготовить структурированные метки (tags, class, topic, category, subclass и т.д.)
    """

    def __init__(self):
        self.document_classifier = DocumentClassifierAgent()
        self.domain_classifier = DomainClassifierAgent()
        self.taxonomy_mapper = TaxonomyMapperAgent()
        self.tagging_agent = TaggingAgent()

    def categorize(self, text: str, metadata: dict = None) -> dict:
        """
        Categorize the document by analyzing its content and metadata.

        Args:
            text: The document text to categorize
            metadata: Optional metadata about the document

        Returns:
            A dictionary containing categorization results
        """
        document_type = self.document_classifier.classify(text)
        domain = self.domain_classifier.classify(text)
        taxonomy = self.taxonomy_mapper.map(text, document_type, domain)
        tags = self.tagging_agent.extract(text)

        return {
            "document_type": document_type,
            "domain": domain,
            "taxonomy": taxonomy,
            "tags": tags
        }

