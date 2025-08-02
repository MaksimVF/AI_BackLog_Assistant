



"""
Test script for the complete pipeline architecture
"""

from pipelines import (
    InputProcessingPipeline,
    InformationManipulationPipeline,
    OutputPipeline,
    MainPipelineCoordinator
)

def test_pipeline_architecture():
    """Test the complete pipeline architecture"""

    print("Testing pipeline architecture...")

    # Create coordinator
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
    success = test_pipeline_architecture()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")



