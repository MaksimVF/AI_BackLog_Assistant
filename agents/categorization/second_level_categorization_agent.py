






"""
Second Level Categorization Agent
"""

from .second_level_categorization.domain_router import categorize_document_by_domain
from tools.llm_tool import LLMTool
from config.settings import EMBEDDING_MODEL_NAME

class SecondLevelCategorizationAgent:
    """
    Performs second-level categorization of documents after initial domain detection.

    This agent routes documents to domain-specific categorizers for more granular
    classification within a specific domain. It includes fallback to LLM for low-confidence
    categorizations.
    """

    def __init__(self, confidence_threshold=0.6):
        """
        Initialize the categorization agent.

        Args:
            confidence_threshold: Minimum confidence score to accept embedding-based
                                categorization without LLM fallback (default: 0.6)
        """
        self.confidence_threshold = confidence_threshold
        self.llm_tool = LLMTool()

    def categorize(self, document: str, domain: str) -> dict:
        """
        Categorizes a document within a specific domain.

        Args:
            document: The document text to categorize
            domain: The detected domain (e.g., "it", "finance")

        Returns:
            Dictionary containing categorization results:
            {
                "domain": str,
                "category": str,
                "confidence": float,
                "source": str
            }
        """
        return categorize_document_by_domain(document, domain)

    def categorize_with_fallback(self, document: str, domain: str) -> dict:
        """
        Categorizes a document with fallback to LLM if confidence is low.

        Args:
            document: The document text to categorize
            domain: The detected domain

        Returns:
            Categorization result with potentially improved confidence via LLM
        """
        # First attempt with embedding-based categorization
        result = self.categorize(document, domain)

        # Check if we need LLM fallback
        if result["confidence"] < self.confidence_threshold:
            try:
                # Use LLM to verify or improve categorization
                llm_result = self._llm_categorization(document, domain)

                # If LLM provides a different category with higher confidence, use it
                if (llm_result["confidence"] > result["confidence"] or
                    llm_result["confidence"] >= self.confidence_threshold):
                    return {
                        "domain": domain,
                        "category": llm_result["category"],
                        "confidence": llm_result["confidence"],
                        "source": f"llm_fallback_{result['source']}"
                    }
            except Exception as e:
                print(f"LLM fallback failed, using original result: {e}")

        return result

    def _llm_categorization(self, document: str, domain: str) -> dict:
        """
        Uses LLM to categorize a document within a specific domain.

        Args:
            document: The document text to categorize
            domain: The detected domain

        Returns:
            LLM-based categorization result
        """
        # Prepare prompt for LLM
        prompt = f"""
        You are an expert in {domain} document categorization. Analyze the following document
        and classify it into one of the categories for the {domain} domain. Provide only the category
        name and a confidence score (0-1) in JSON format.

        Document:
        {document}

        JSON format:
        {{"category": "detected_category", "confidence": 0.95}}
        """

        # Get LLM response
        response = self.llm_tool.generate_response(prompt)

        # Parse the response (simple parsing, could be improved with proper JSON parsing)
        try:
            # Try to extract JSON from the response
            import json
            import re

            # Look for JSON pattern in the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(0))
                return result
            else:
                # If no JSON found, create a fallback result
                return {
                    "category": "unknown",
                    "confidence": 0.5
                }
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return {
                "category": "unknown",
                "confidence": 0.5
            }





