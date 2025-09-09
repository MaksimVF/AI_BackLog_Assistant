


from typing import Dict, Optional
import uuid
from datetime import datetime
from langdetect import detect
from .context_classifier import ContextClassifier
from .intent_identifier import IntentIdentifier

class MetadataBuilder:
    """
    Builds comprehensive metadata for input data, including:
    - Basic metadata (ID, timestamp, source, etc.)
    - Context classification
    - Intent identification
    - Language detection
    - Future extensions (domain, confidence, format, etc.)
    """

    def __init__(self):
        self.context_classifier = ContextClassifier()
        self.intent_identifier = IntentIdentifier()

    def build_metadata(self, user_input: Dict) -> Dict:
        """
        Generate comprehensive metadata for user input

        Args:
            user_input: Dictionary containing 'user_id', 'text', 'source' (optional)

        Returns:
            Dictionary with comprehensive metadata
        """
        # Basic metadata
        metadata = {
            "id": str(uuid.uuid4()),
            "user_id": user_input.get("user_id"),
            "timestamp": datetime.utcnow().isoformat(),
            "source": user_input.get("source", "unknown"),
            "input_length": len(user_input.get("text", "")),
        }

        # Language detection
        text = user_input.get("text", "")
        if text:
            try:
                metadata["language"] = detect(text)
            except:
                metadata["language"] = "unknown"
        else:
            metadata["language"] = "unknown"

        # Context classification
        context_analysis = self.context_classifier.classify(text)
        metadata["context"] = context_analysis.context
        metadata["context_confidence"] = context_analysis.confidence

        # Intent identification
        intent_analysis = self.intent_identifier.identify(text)
        metadata["intent"] = intent_analysis.intent_type
        metadata["intent_confidence"] = intent_analysis.confidence

        # Additional metadata (placeholders for future extensions)
        metadata["domain"] = self._infer_domain(context_analysis.context)
        metadata["confidence_level"] = self._calculate_confidence(
            context_analysis.confidence,
            intent_analysis.confidence
        )
        metadata["format"] = self._infer_format(text)

        return metadata

    def _infer_domain(self, context: str) -> str:
        """Infers domain based on context"""
        domain_mapping = {
            "финансовый": "finance",
            "юридический": "legal",
            "медицинский": "medical",
            "бытовой": "household",
            "технический": "technical"
        }
        return domain_mapping.get(context, "general")

    def _calculate_confidence(self, context_confidence: float, intent_confidence: float) -> str:
        """Calculates overall confidence level"""
        avg_confidence = (context_confidence + intent_confidence) / 2
        if avg_confidence > 0.8:
            return "high"
        elif avg_confidence > 0.5:
            return "medium"
        else:
            return "low"

    def _infer_format(self, text: str) -> str:
        """Infers input format based on text characteristics"""
        if not text:
            return "unknown"

        # Simple heuristics for format detection
        if text.count("\n") > 2:
            return "multiline"
        elif "?" in text:
            return "question"
        elif text.count(" ") > 10:
            return "description"
        else:
            return "short"

    def build_metadata_for_storage(self, user_input: Dict) -> Dict:
        """
        Build metadata specifically for storage systems like Weaviate

        Args:
            user_input: Dictionary containing input data

        Returns:
            Dictionary formatted for storage
        """
        metadata = self.build_metadata(user_input)

        # Format for Weaviate storage
        return {
            "content": user_input.get("text", ""),
            "source_type": metadata["source"],
            "source_name": user_input.get("source_name", "unknown"),
            "timestamp": metadata["timestamp"],
            "metadata": {
                "user_id": metadata["user_id"],
                "language": metadata["language"],
                "context": metadata["context"],
                "context_confidence": metadata["context_confidence"],
                "intent": metadata["intent"],
                "intent_confidence": metadata["intent_confidence"],
                "domain": metadata["domain"],
                "confidence_level": metadata["confidence_level"],
                "format": metadata["format"],
                "input_length": metadata["input_length"]
            }
        }


