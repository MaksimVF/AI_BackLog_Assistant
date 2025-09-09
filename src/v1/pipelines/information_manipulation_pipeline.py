


"""
Information Manipulation Pipeline (IMP)

Coordinates the flow of data through information manipulation agents:
1. ResultAggregatorAgent
2. ContextEnricherAgent
3. PrioritizationAgent
4. CriticalityClassifierAgent
5. BottleneckDetectorAgent
6. ScoringAgent
7. DecisionMakerAgent
8. MetadataEnricherAgent
9. QualityAssuranceAgent

Input: Structured data from IPP
Output: Enriched, analyzed data ready for output
"""

from typing import Dict, Any
from pydantic import BaseModel, validator
from agents.prioritization.prioritization_agent import PrioritizationAgent
from agents.prioritization.criticality_classifier import CriticalityClassifierAgent
from agents.prioritization.bottleneck_detector import BottleneckDetectorAgent
from agents.prioritization.scoring_agent import ScoringAgent
from agents.prioritization.decision_agent import DecisionMakerAgent
from agents.imp.result_aggregator_agent import ResultAggregatorAgent
from agents.imp.context_enricher_agent import ContextEnricherAgent
from agents.imp.metadata_enricher_agent import MetadataEnricherAgent
from agents.imp.quality_assurance_agent import QualityAssuranceAgent
from .base_pipeline import BasePipeline, PipelineConfig

class IMPInputSchema(BaseModel):
    """Input schema for IMP"""
    document_id: str
    raw_text: str
    modality: str
    entities: Dict[str, Any]
    intent: str
    metadata: Dict[str, Any]

    @validator('document_id')
    def document_id_not_empty(cls, v):
        if not v:
            raise ValueError("document_id cannot be empty")
        return v

class IMPOutputSchema(BaseModel):
    """Output schema for IMP"""
    document_id: str
    processed_text: str
    analysis: Dict[str, Any]
    metadata: Dict[str, Any]
    quality: Dict[str, Any]

    @validator('analysis')
    def analysis_has_required_fields(cls, v):
        required_fields = ['priority', 'criticality', 'scores', 'decision']
        for field in required_fields:
            if field not in v:
                raise ValueError(f"Analysis missing required field: {field}")
        return v

class InformationManipulationPipeline(BasePipeline):
    """
    Information Manipulation Pipeline Coordinator
    """

    def __init__(self, config: PipelineConfig = None):
        super().__init__(config)
        self.result_aggregator = ResultAggregatorAgent()
        self.context_enricher = ContextEnricherAgent()
        self.prioritization_agent = PrioritizationAgent()
        self.criticality_classifier = CriticalityClassifierAgent()
        self.bottleneck_detector = BottleneckDetectorAgent()
        self.scoring_agent = ScoringAgent()
        self.decision_maker = DecisionMakerAgent()
        self.metadata_enricher = MetadataEnricherAgent()
        self.quality_assurance = QualityAssuranceAgent()

    def _validate_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input data against IMPInputSchema"""
        try:
            validated = IMPInputSchema(**data).dict()
            return validated
        except Exception as e:
            self._log(f"Input validation failed: {e}", "error")
            raise

    def _validate_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate output data against IMPOutputSchema"""
        try:
            validated = IMPOutputSchema(**data).dict()
            return validated
        except Exception as e:
            self._log(f"Output validation failed: {e}", "error")
            raise

    def _process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through the IMP pipeline.

        Steps:
        1. Aggregate results
        2. Enrich context
        3. Prioritize
        4. Classify criticality
        5. Detect bottlenecks
        6. Score
        7. Make decision
        8. Enrich metadata
        9. Quality assurance
        """
        document_id = data['document_id']
        raw_text = data['raw_text']
        modality = data['modality']
        entities = data['entities']
        intent = data['intent']
        metadata = data['metadata']

        # Step 1: Aggregate results
        self._log(f"Processing document {document_id}: Aggregating results")
        aggregated_results = self.result_aggregator.aggregate(
            document_id=document_id,
            raw_text=raw_text,
            modality=modality,
            entities=entities,
            intent=intent,
            metadata=metadata
        )

        # Step 2: Enrich context
        self._log(f"Processing document {document_id}: Enriching context")
        enriched_data = self.context_enricher.enrich(
            document_id=document_id,
            aggregated_results=aggregated_results
        )

        # Step 3: Prioritize
        self._log(f"Processing document {document_id}: Prioritizing")
        priority_data = self.prioritization_agent.prioritize(enriched_data)

        # Step 4: Classify criticality
        self._log(f"Processing document {document_id}: Classifying criticality")
        criticality_data = self.criticality_classifier.classify(enriched_data)

        # Step 5: Detect bottlenecks
        self._log(f"Processing document {document_id}: Detecting bottlenecks")
        bottleneck_data = self.bottleneck_detector.detect(enriched_data)

        # Step 6: Score
        self._log(f"Processing document {document_id}: Scoring")
        scoring_data = self.scoring_agent.score_task({
            'document_id': document_id,
            'priority': priority_data['priority'],
            'criticality': criticality_data['criticality'],
            'bottlenecks': bottleneck_data['bottlenecks']
        })

        # Step 7: Make decision
        self._log(f"Processing document {document_id}: Making decision")
        decision_data = self.decision_maker.make_decision({
            'document_id': document_id,
            'priority': priority_data['priority'],
            'criticality': criticality_data['criticality'],
            'scores': scoring_data,
            'context': enriched_data['context']
        })

        # Step 8: Enrich metadata
        self._log(f"Processing document {document_id}: Enriching metadata")
        enriched_metadata = self.metadata_enricher.enrich(
            document_id=document_id,
            original_metadata=metadata,
            priority=priority_data['priority'],
            criticality=criticality_data['criticality'],
            decision=decision_data['decision']
        )

        # Step 9: Quality assurance
        self._log(f"Processing document {document_id}: Quality assurance")
        quality_data = self.quality_assurance.assess_quality({
            'document_id': document_id,
            'processed_data': enriched_data,
            'analysis_results': {
                'priority': priority_data,
                'criticality': criticality_data,
                'scoring': scoring_data,
                'decision': decision_data
            }
        })

        return {
            'document_id': document_id,
            'processed_text': enriched_data['processed_text'],
            'analysis': {
                'priority': priority_data['priority'],
                'criticality': criticality_data['criticality'],
                'bottlenecks': bottleneck_data['bottlenecks'],
                'scores': scoring_data,
                'decision': decision_data['decision']
            },
            'metadata': enriched_metadata,
            'quality': quality_data
        }


