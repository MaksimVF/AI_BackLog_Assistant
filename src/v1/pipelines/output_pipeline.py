


"""
Output Pipeline (OP)

Coordinates the flow of data through output agents:
1. SummaryAgent
2. OutputAgent
3. FormatAdapter
4. ResponseFormatter
5. OutputSanitizer

Input: Enriched, analyzed data from IMP
Output: Final formatted results for delivery
"""

from typing import Dict, Any
from pydantic import BaseModel, validator
from agents.summary.summary_agent import SummaryAgent
from agents.output.output_agent import OutputAgent
from agents.output.format_adapter import FormatAdapter
from agents.output.response_formatter import ResponseFormatter
from agents.output.output_sanitizer import OutputSanitizer
from .base_pipeline import BasePipeline, PipelineConfig

class OPInputSchema(BaseModel):
    """Input schema for OP"""
    document_id: str
    processed_text: str
    analysis: Dict[str, Any]
    metadata: Dict[str, Any]
    quality: Dict[str, Any]

    @validator('document_id')
    def document_id_not_empty(cls, v):
        if not v:
            raise ValueError("document_id cannot be empty")
        return v

class OPOutputSchema(BaseModel):
    """Output schema for OP"""
    document_id: str
    summary: str
    key_points: list
    recommendations: list
    formatted_output: Any
    delivery_format: str

    @validator('delivery_format')
    def valid_format(cls, v):
        valid_formats = ['json', 'html', 'pdf', 'text', 'markdown']
        if v not in valid_formats:
            raise ValueError(f"Invalid delivery format: {v}")
        return v

class OutputPipeline(BasePipeline):
    """
    Output Pipeline Coordinator
    """

    def __init__(self, config: PipelineConfig = None):
        super().__init__(config)
        self.summary_agent = SummaryAgent()
        self.output_agent = OutputAgent(
            mode="API",  # Default mode
            user_profile={},
            compact_mode=True
        )
        self.format_adapter = FormatAdapter()
        self.response_formatter = ResponseFormatter()
        self.output_sanitizer = OutputSanitizer()

    def _validate_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input data against OPInputSchema"""
        try:
            validated = OPInputSchema(**data).dict()
            return validated
        except Exception as e:
            self._log(f"Input validation failed: {e}", "error")
            raise

    def _validate_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate output data against OPOutputSchema"""
        try:
            validated = OPOutputSchema(**data).dict()
            return validated
        except Exception as e:
            self._log(f"Output validation failed: {e}", "error")
            raise

    def _process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through the OP pipeline.

        Steps:
        1. Generate summary
        2. Format output
        3. Adapt format
        4. Sanitize output
        """
        document_id = data['document_id']
        processed_text = data['processed_text']
        analysis = data['analysis']
        metadata = data['metadata']
        quality = data['quality']

        # Step 1: Generate summary
        self._log(f"Processing document {document_id}: Generating summary")
        summary_data = self.summary_agent.generate_summary(processed_text)

        # Step 2: Format output using OutputAgent
        self._log(f"Processing document {document_id}: Formatting output")
        formatted_output = self.output_agent.process(
            task_id=document_id,
            decision_result=analysis['decision'],
            priority_data=analysis.get('priority', {}),
            effort_data={},  # Would come from analysis if available
            deadline=metadata.get('deadline', 'N/A'),
            visuals=None,  # Would come from analysis if available
            schedule=None  # Would come from analysis if available
        )

        # Step 3: Adapt format if needed
        self._log(f"Processing document {document_id}: Adapting format")
        adapted_output = self.format_adapter.transform(formatted_output)

        # Step 4: Sanitize output
        self._log(f"Processing document {document_id}: Sanitizing output")
        sanitized_output = self.output_sanitizer.sanitize(adapted_output)

        return {
            'document_id': document_id,
            'summary': summary_data['summary'],
            'key_points': summary_data['keypoints'],
            'recommendations': analysis.get('recommendations', []),
            'formatted_output': sanitized_output,
            'delivery_format': 'json'  # Default format
        }

