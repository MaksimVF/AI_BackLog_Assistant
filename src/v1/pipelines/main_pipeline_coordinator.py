



"""
Main Pipeline Coordinator

Coordinates the end-to-end flow through all three pipelines:
1. Input Processing Pipeline (IPP)
2. Information Manipulation Pipeline (IMP)
3. Output Pipeline (OP)

With async processing support for improved performance.
"""

from typing import Dict, Any, Optional, Coroutine, List
import asyncio
from .input_processing_pipeline import InputProcessingPipeline
from .information_manipulation_pipeline import InformationManipulationPipeline
from .output_pipeline import OutputPipeline
from .base_pipeline import PipelineConfig
from utils.async_utils import AsyncPipelineProcessor, run_sync_in_executor

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

    async def process_end_to_end_async(
        self,
        document_id: str,
        raw_content: Any,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process data through all pipelines end-to-end with async support.

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

        # Run pipelines with async support
        async_processor = AsyncPipelineProcessor(concurrency_limit=3)

        # Convert sync pipeline methods to async
        async def run_ipp(data):
            return await run_sync_in_executor(self.ipp.process)(data)

        async def run_imp(data):
            return await run_sync_in_executor(self.imp.process)(data)

        async def run_op(data):
            return await run_sync_in_executor(self.op.process)(data)

        # Process through all stages asynchronously
        result = await async_processor.process_stages(
            ipp_input,
            [run_ipp, run_imp, run_op]
        )

        return result

    async def process_parallel_pipelines(
        self,
        documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Process multiple documents in parallel using async.

        Args:
            documents: List of documents to process, each with document_id, raw_content, metadata

        Returns:
            List of processed outputs
        """
        async def process_single_doc(doc):
            return await self.process_end_to_end_async(
                doc['document_id'],
                doc['raw_content'],
                doc.get('metadata')
            )

        # Process all documents with controlled concurrency
        async_processor = AsyncPipelineProcessor(concurrency_limit=5)
        tasks = [process_single_doc(doc) for doc in documents]

        return await async_processor.process_parallel_stages(None, tasks)


    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        pass



