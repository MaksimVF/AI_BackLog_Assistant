

"""
Result Aggregator Agent

Aggregates results from IPP agents to create a unified data structure
for further processing in the IMP pipeline.
"""

from typing import Dict, Any
from pydantic import BaseModel

class AggregatedResult(BaseModel):
    """Structure for aggregated results"""
    document_id: str
    processed_text: str
    modality: str
    entities: Dict[str, Any]
    intent: str
    context: Dict[str, Any] = {}
    metadata: Dict[str, Any]

class ResultAggregatorAgent:
    """
    Aggregates results from IPP agents into a unified structure.
    """

    def aggregate(
        self,
        document_id: str,
        raw_text: str,
        modality: str,
        entities: Dict[str, Any],
        intent: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Aggregate results from IPP processing.

        Args:
            document_id: Unique document identifier
            raw_text: Processed text content
            modality: Content modality (text/audio/video)
            entities: Extracted entities
            intent: Identified intent
            metadata: Metadata from IPP

        Returns:
            Aggregated result structure
        """
        # Create basic context from available data
        context = {
            'modality': modality,
            'intent': intent,
            'entity_types': list(entities.keys()) if entities else []
        }

        # Create aggregated result
        result = AggregatedResult(
            document_id=document_id,
            processed_text=raw_text,
            modality=modality,
            entities=entities,
            intent=intent,
            context=context,
            metadata=metadata
        )

        return result.dict()

