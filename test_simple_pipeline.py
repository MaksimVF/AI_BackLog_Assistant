


"""
Simple test script for the pipeline architecture without external dependencies
"""

from pipelines.base_pipeline import BasePipeline, PipelineConfig

class TestPipeline(BasePipeline):
    """Test pipeline implementation"""

    def _process(self, data):
        """Simple processing that just echoes the input"""
        return {"processed": True, "input_data": data}

def test_base_pipeline():
    """Test the base pipeline functionality"""

    # Create a test pipeline
    config = PipelineConfig(enable_logging=True)
    pipeline = TestPipeline(config)

    # Test data
    test_input = {"test": "data"}

    try:
        # Process the data
        result = pipeline.process(test_input)
        print("Base pipeline test successful!")
        print(f"Result: {result}")
        return True

    except Exception as e:
        print(f"Base pipeline test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_base_pipeline()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")

