



"""
Test script for the main pipeline coordinator without external dependencies
"""

from pipelines.base_pipeline import BasePipeline, PipelineConfig

class MockIPPPipeline(BasePipeline):
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

class MockIMPPipeline(BasePipeline):
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

class MockOPPipeline(BasePipeline):
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
        self.ipp = MockIPPPipeline()
        self.imp = MockIMPPipeline()
        self.op = MockOPPipeline()

    def process_end_to_end(self, document_id, raw_content, metadata=None):
        """Process data through all mock pipelines"""

        # Process through IPP
        ipp_input = {
            'document_id': document_id,
            'raw_content': raw_content,
            'metadata': metadata or {}
        }
        ipp_output = self.ipp.process(ipp_input)

        # Process through IMP
        imp_output = self.imp.process(ipp_output)

        # Process through OP
        op_output = self.op.process(imp_output)

        return op_output

def test_mock_coordinator():
    """Test the mock pipeline coordinator"""

    # Create coordinator
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
        # Process through complete pipeline
        result = coordinator.process_end_to_end(
            document_id=test_data['document_id'],
            raw_content=test_data['raw_content'],
            metadata=test_data['metadata']
        )

        print("Mock pipeline coordinator test successful!")
        print(f"Document ID: {result.get('document_id')}")
        print(f"Summary: {result.get('summary', 'No summary')}")
        print(f"Key Points: {result.get('key_points', [])}")
        print(f"Delivery Format: {result.get('delivery_format', 'Unknown')}")

        return True

    except Exception as e:
        print(f"Mock pipeline coordinator test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_mock_coordinator()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")


