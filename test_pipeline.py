

"""
Test script for the pipeline architecture
"""

from pipelines.main_pipeline_coordinator import MainPipelineCoordinator

def test_pipeline():
    """Test the complete pipeline with sample data"""

    # Create pipeline coordinator
    coordinator = MainPipelineCoordinator()

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

        print("Pipeline processing successful!")
        print(f"Document ID: {result.get('document_id')}")
        print(f"Summary: {result.get('summary', 'No summary')}")
        print(f"Key Points: {result.get('key_points', [])}")
        print(f"Delivery Format: {result.get('delivery_format', 'Unknown')}")

        return True

    except Exception as e:
        print(f"Pipeline processing failed: {e}")
        return False

if __name__ == "__main__":
    success = test_pipeline()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")

