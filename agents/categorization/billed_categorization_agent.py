


"""
Billed Categorization Agent

Wrapper around CategorizationAgent that includes billing checks.
"""

from .categorization_agent import CategorizationAgent
from web_server.billing_middleware import billing_required

class BilledCategorizationAgent:
    """
    Billed version of CategorizationAgent that includes billing checks.

    This wrapper ensures that billing is properly handled before executing
    the categorization functionality.
    """

    def __init__(self):
        self.agent = CategorizationAgent()

    @billing_required("CategorizationAgent", units=1)
    def categorize_document(self, document_text: str, metadata: dict = None) -> dict:
        """
        Perform comprehensive categorization of the document with billing.

        Args:
            document_text: The document text to categorize
            metadata: Optional metadata about the document

        Returns:
            A dictionary containing all categorization results
        """
        return self.agent.categorize_document(document_text, metadata)

    @billing_required("CategorizationAgent", units=1)
    def categorize_batch(self, documents: list) -> list:
        """
        Categorize a batch of documents with billing.

        Args:
            documents: List of documents to categorize

        Returns:
            List of categorization results
        """
        results = []
        for doc in documents:
            result = self.agent.categorize_document(doc['text'], doc.get('metadata'))
            results.append(result)
        return results


