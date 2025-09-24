





"""
Interactive Feedback Agent

Provides interactive questioning and feedback collection for:
- Clarifying ambiguous classifications
- Collecting user preferences
- Providing improvement suggestions
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class InteractiveFeedbackAgent:
    """Provides interactive feedback and questioning"""

    def __init__(self):
        """Initialize interactive feedback agent"""
        self.questions = []
        self.suggestions = []

    def ask_clarifying_question(self, document_id: str, classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ask clarifying question about classification

        Args:
            document_id: ID of the document
            classification: Classification result

        Returns:
            Clarifying question and options
        """
        category = classification.get("category", "unknown")
        confidence = classification.get("confidence", 0.5)

        if confidence < 0.6:
            question = {
                "document_id": document_id,
                "question": f"The document was classified as '{category}' with low confidence. Is this correct?",
                "options": ["Yes", "No", "Not sure"],
                "type": "classification"
            }
        else:
            question = {
                "document_id": document_id,
                "question": f"The document was classified as '{category}'. Does this seem accurate?",
                "options": ["Yes", "No", "Mostly"],
                "type": "classification"
            }

        self.questions.append(question)
        logger.info(f"Generated clarifying question for {document_id}")

        return question

    def ask_prioritization_question(self, document_id: str, prioritization: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ask clarifying question about prioritization

        Args:
            document_id: ID of the document
            prioritization: Prioritization result

        Returns:
            Clarifying question and options
        """
        priority = prioritization.get("priority_level", "medium")
        score = prioritization.get("priority_score", 0.5)

        question = {
            "document_id": document_id,
            "question": f"The document was prioritized as '{priority}'. Does this seem appropriate?",
            "options": ["Yes", "No", "Should be higher", "Should be lower"],
            "type": "prioritization"
        }

        self.questions.append(question)
        logger.info(f"Generated prioritization question for {document_id}")

        return question

    def provide_improvement_suggestion(self, document_id: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide improvement suggestion

        Args:
            document_id: ID of the document
            analysis: Analysis result

        Returns:
            Improvement suggestion
        """
        quality = analysis.get("quality_score", 0.5)
        issues = analysis.get("issues", [])

        if quality < 0.6:
            suggestion = {
                "document_id": document_id,
                "suggestion": "The document quality is low. Consider providing more details or clarifying the content.",
                "issues": issues,
                "type": "improvement"
            }
        else:
            suggestion = {
                "document_id": document_id,
                "suggestion": "The document quality is good. Consider adding more specific details for better analysis.",
                "issues": issues,
                "type": "improvement"
            }

        self.suggestions.append(suggestion)
        logger.info(f"Generated improvement suggestion for {document_id}")

        return suggestion

    def collect_user_response(self, question_id: int, response: str) -> Dict[str, Any]:
        """
        Collect user response to a question

        Args:
            question_id: ID of the question
            response: User response

        Returns:
            Response collection result
        """
        if question_id < 0 or question_id >= len(self.questions):
            return {"status": "error", "message": "Invalid question ID"}

        question = self.questions[question_id]
        question["response"] = response
        question["processed"] = False

        logger.info(f"Collected response for question {question_id}: {response}")

        return {
            "status": "collected",
            "question_id": question_id,
            "response": response
        }

    def process_responses(self) -> Dict[str, Any]:
        """
        Process collected responses

        Returns:
            Response processing summary
        """
        processed = 0
        unprocessed = 0

        for question in self.questions:
            if "response" in question:
                if question["response"] == "No":
                    # Mark for further processing
                    question["processed"] = True
                    processed += 1
                else:
                    unprocessed += 1

        logger.info(f"Processed {processed} responses, {unprocessed} unprocessed")

        return {
            "processed": processed,
            "unprocessed": unprocessed,
            "total": len(self.questions)
        }






