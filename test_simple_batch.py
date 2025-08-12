


"""
Simple test script to demonstrate batch processing capabilities
"""

import time
from utils.batch_processor import BatchProcessor, AgentBatchProcessor, batch_registry
from utils.batch_decorator import batch_processing

# Simple test class with batch processing
class TestClassifier:
    """Simple test classifier for demonstration"""

    @batch_processing(agent_type="test_classifier", batch_size=2, max_wait_time=1.0)
    def classify(self, text: str) -> str:
        """Classify text (simulated)"""
        # Simulate some processing time
        time.sleep(0.5)
        if "договор" in text.lower():
            return "contract"
        elif "счет" in text.lower():
            return "invoice"
        else:
            return "other"

def test_batch_processing():
    """Test batch processing with a simple classifier"""
    print("Testing Batch Processing...")

    classifier = TestClassifier()

    # Test documents
    documents = [
        "Договор аренды недвижимости",
        "Счет на оплату №12345",
        "Протокол собрания акционеров",
        "Трудовой договор с сотрудником",
        "Устав организации",
        "Заявление на отпуск"
    ]

    start_time = time.time()
    results = []

    # Process documents (will be batched automatically)
    for doc in documents:
        result = classifier.classify(doc)
        results.append((doc, result))
        print(f"Processed: {doc} -> {result}")

    end_time = time.time()

    print(f"\nProcessed {len(documents)} documents in {end_time - start_time:.2f} seconds")
    print("This demonstrates batch processing - multiple documents were processed together")

    # Show batch processor stats
    stats = batch_registry.get_all_stats()
    print("\nBatch Processor Statistics:")
    for agent_type, stat in stats.items():
        print(f"  {agent_type}: {stat.get('processed_count', 0)} requests processed")

def test_direct_batch_processor():
    """Test the batch processor directly"""
    print("\nTesting Direct Batch Processor...")

    # Create a custom batch processor
    def custom_process_function(batch_data):
        """Custom process function for batch"""
        results = []
        for data in batch_data:
            text = data.get("text", "")
            # Simulate processing
            time.sleep(0.3)
            if "important" in text.lower():
                results.append({"result": "HIGH_PRIORITY", "text": text})
            else:
                results.append({"result": "NORMAL", "text": text})
        return results

    processor = AgentBatchProcessor(
        agent_type="custom_processor",
        batch_size=3,
        max_wait_time=1.5
    )

    # Override the process function
    processor.processor.process_function = custom_process_function

    # Submit some requests
    test_data = [
        {"text": "This is an important document"},
        {"text": "Regular document content"},
        {"text": "Another important file"},
        {"text": "Normal text here"},
        {"text": "High priority content"}
    ]

    start_time = time.time()
    all_results = []

    def handle_result(result):
        """Handle individual result"""
        print(f"  Result received: {result}")
        all_results.append(result)

    # Submit all requests
    for data in test_data:
        processor.submit(data, handle_result)
        time.sleep(0.1)  # Small delay between submissions

    # Wait a bit for processing to complete
    time.sleep(3)

    end_time = time.time()
    print(f"Processed {len(all_results)} items in {end_time - start_time:.2f} seconds")

    # Show stats
    stats = processor.get_stats()
    print(f"Custom processor stats: {stats['processed_count']} processed")

def main():
    """Main test function"""
    print("Starting Simple Batch Processing Test...")
    print("=" * 50)

    try:
        test_batch_processing()
        test_direct_batch_processor()

        print("\n" + "=" * 50)
        print("Simple Batch Processing Test Completed!")

    except Exception as e:
        print(f"Error during testing: {str(e)}")
    finally:
        # Cleanup
        from utils.batch_processor import shutdown_all_processors
        shutdown_all_processors()
        print("Batch processors shutdown.")

if __name__ == "__main__":
    main()


