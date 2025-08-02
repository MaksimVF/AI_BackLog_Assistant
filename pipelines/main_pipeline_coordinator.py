



"""
Main Pipeline Coordinator

Coordinates the end-to-end flow through all three pipelines:
1. Input Processing Pipeline (IPP)
2. Information Manipulation Pipeline (IMP)
3. Output Pipeline (OP)
"""

from typing import Dict, Any, Optional
from .input_processing_pipeline import InputProcessingPipeline
from .information_manipulation_pipeline import InformationManipulationPipeline
from .output_pipeline import OutputPipeline
from .base_pipeline import PipelineConfig

class MainPipelineCoordinator:
    """
    Main coordinator for all pipelines.
    """

    def __init__(
        self,
        ipp_config: Optional[PipelineConfig] = None,
        imp_config: Optional[PipelineConfig] = None,
        op_config: Optional[PipelineConfig] = None
    ):
        """
        Initialize the main coordinator with pipeline configurations.

        Args:
            ipp_config: Configuration for Input Processing Pipeline
            imp_config: Configuration for Information Manipulation Pipeline
            op_config: Configuration for Output Pipeline
        """
        self.ipp = InputProcessingPipeline(ipp_config)
        self.imp = InformationManipulationPipeline(imp_config)
        self.op = OutputPipeline(op_config)

    def process_end_to_end(
        self,
        document_id: str,
        raw_content: Any,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process data through all pipelines end-to-end.

        Args:
            document_id: Unique document identifier
            raw_content: Raw input content (text, audio, video)
            metadata: Optional initial metadata

        Returns:
            Final processed output
        """
        # Prepare input for IPP
        ipp_input = {
            'document_id': document_id,
            'raw_content': raw_content,
            'metadata': metadata or {}
        }

        # Process through IPP
        ipp_output = self.ipp.process(ipp_input)

        # Process through IMP
        imp_output = self.imp.process(ipp_output)

        # Process through OP
        op_output = self.op.process(imp_output)

        return op_output

    def process_ipp(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through Input Processing Pipeline only.

        Args:
            data: Input data for IPP

        Returns:
            IPP output
        """
        return self.ipp.process(data)

    def process_imp(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through Information Manipulation Pipeline only.

        Args:
            data: Input data for IMP

        Returns:
            IMP output
        """
        return self.imp.process(data)

    def process_op(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through Output Pipeline only.

        Args:
            data: Input data for OP

        Returns:
            OP output
        """
        return self.op.process(data)

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        pass



