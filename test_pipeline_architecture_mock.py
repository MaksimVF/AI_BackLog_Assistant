




"""
Test script for the complete pipeline architecture using mock implementations
"""

from pipelines.base_pipeline import BasePipeline, PipelineConfig
from pipelines.main_pipeline_coordinator import MainPipelineCoordinator

class MockInputProcessingPipeline(BasePipeline):
    """Mock IPP pipeline"""

    def _process(self, data):
        """Mock IPP processing"""
        return {
            "document_id": data.get("document_id", "mock_doc"),
            "raw_text": data.get("raw_content", "mock text"),
            "modality": "text",
            "entities": {"mock_entities": ["entity1", "entity2"]},
            "intent": "mock_intent",
            "metadata": data.get("metadata", {})
        }

class MockInformationManipulationPipeline(BasePipeline):
    """Mock IMP pipeline"""

    def _process(self, data):
        """Mock IMP processing"""
        return {
            "document_id": data.get("document_id", "mock_doc"),
            "processed_text": data.get("raw_text", "mock text"),
            "analysis": {
                "priority": "medium",
                "criticality": "normal",
                "bottlenecks": [],
                "scores": {"priority_score": 5.0, "criticality_score": 3.0},
                "decision": "proceed"
            },
            "metadata": data.get("metadata", {}),
            "quality": {"completeness": 90, "accuracy": 85}
        }

class MockOutputPipeline(BasePipeline):
    """Mock OP pipeline"""

    def _process(self, data):
        """Mock OP processing"""
        return {
            "document_id": data.get("document_id", "mock_doc"),
            "summary": "Mock summary of the document",
            "key_points": ["Point 1", "Point 2", "Point 3"],
            "recommendations": ["Recommendation 1"],
            "formatted_output": "Final formatted result",
            "delivery_format": "json"
        }

class MockMainPipelineCoordinator:
    """Mock main pipeline coordinator"""

    def __init__(self):
        self.ipp = MockInputProcessingPipeline()
        self.imp = MockInformationManipulationPipeline()
        self.op = MockOutputPipeline()

    def process_ipp(self, data):
        """Process data through IPP"""
        return self.ipp.process(data)

    def process_imp(self, data):
        """Process data through IMP"""
        return self.imp.process(data)

    def process_op(self, data):
        """Process data through OP"""
        return self.op.process(data)

    def process_end_to_end(self, document_id, raw_content, metadata=None):
        """Process data through all mock pipelines"""

        # Process through IPP
        ipp_input = {
            'document_id': document_id,
            'raw_content': raw_content,
            'metadata': metadata or {}
        }
        ipp_output = self.process_ipp(ipp_input)

        # Process through IMP
        imp_output = self.process_imp(ipp_output)

        # Process through OP
        op_output = self.process_op(imp_output)

        return op_output

def test_mock_pipeline_architecture():
    """Test the complete pipeline architecture using mocks"""

    print("Testing pipeline architecture with mock implementations...")

    # Create mock coordinator
    coordinator = MockMainPipelineCoordinator()

    # Test data
    test_data = {
        'document_id': 'test_doc_001',
        'raw_content': 'This is a test document about AI pipeline architecture.',
        'metadata': {
            'source': 'test',
            'user': 'test_user'
        }
    }

    try:
        # Test individual pipelines
        print("\n1. Testing Input Processing Pipeline (IPP)...")
        ipp_result = coordinator.process_ipp(test_data)
        print(f"IPP Result: {ipp_result}")

        print("\n2. Testing Information Manipulation Pipeline (IMP)...")
        imp_result = coordinator.process_imp(ipp_result)
        print(f"IMP Result: {imp_result}")

        print("\n3. Testing Output Pipeline (OP)...")
        op_result = coordinator.process_op(imp_result)
        print(f"OP Result: {op_result}")

        # Test end-to-end processing
        print("\n4. Testing end-to-end pipeline processing...")
        e2e_result = coordinator.process_end_to_end(
            document_id=test_data['document_id'],
            raw_content=test_data['raw_content'],
            metadata=test_data['metadata']
        )
        print(f"End-to-End Result: {e2e_result}")

        print("\n✅ All pipeline tests passed!")
        return True

    except Exception as e:
        print(f"\n❌ Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_mock_pipeline_architecture()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")




