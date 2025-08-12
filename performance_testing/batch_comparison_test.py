




"""
Batch Processing Comparison Test

Compare performance between single processing and batch processing.
"""

import time
import random
import threading
from performance_testing.performance_profiler import PerformanceProfiler
from utils.batch_processor import get_batch_processor, shutdown_all_processors

# Sample documents
SAMPLE_DOCUMENTS = [
    "Договор аренды недвижимости",
    "Счет на оплату №12345",
    "Протокол собрания акционеров",
    "Трудовой договор с сотрудником",
    "Устав организации",
    "Заявление на отпуск",
    "Отчет о финансовых результатах",
    "Техническое задание",
    "Коммерческое предложение",
    "Счет-фактура №789"
]

def generate_random_document():
    """Generate a random document from the sample pool"""
    return random.choice(SAMPLE_DOCUMENTS)

# Single processing functions
def single_classify_document():
    """Single document classification"""
    doc = generate_random_document()
    time.sleep(0.15 + random.random() * 0.05)  # Simulate processing
    return {"result": "classified", "document": doc}

def single_summarize_document():
    """Single document summarization"""
    doc = generate_random_document()
    time.sleep(0.25 + random.random() * 0.05)  # Simulate processing
    return {"result": "summarized", "document": doc}

# Batch processing setup
classifier_processor = get_batch_processor("test_classifier", batch_size=3, max_wait_time=0.5)
summarizer_processor = get_batch_processor("test_summarizer", batch_size=2, max_wait_time=0.8)

def batch_classify_document():
    """Batch document classification"""
    doc = generate_random_document()

    # Use a threading event to wait for the result
    result_event = threading.Event()
    result_data = {}

    def callback(result):
        result_data.update(result)
        result_event.set()

    # Submit to batch processor
    classifier_processor.submit({"document": doc}, callback)

    # Wait for result (with timeout)
    if not result_event.wait(timeout=2.0):
        return {"result": "timeout", "document": doc}

    return result_data

def batch_summarize_document():
    """Batch document summarization"""
    doc = generate_random_document()

    # Use a threading event to wait for the result
    result_event = threading.Event()
    result_data = {}

    def callback(result):
        result_data.update(result)
        result_event.set()

    # Submit to batch processor
    summarizer_processor.submit({"document": doc}, callback)

    # Wait for result (with timeout)
    if not result_event.wait(timeout=2.0):
        return {"result": "timeout", "document": doc}

    return result_data

def run_batch_comparison():
    """Run batch processing comparison tests"""
    print("Running Batch Processing Comparison Tests...")
    print("=" * 60)

    profiler = PerformanceProfiler()

    # Test 1: Single Document Classification
    print("\n1. Testing Single Document Classification...")
    profiler.run_test(
        "Single Document Classification",
        single_classify_document,
        duration=10,
        concurrency=1
    )

    # Test 2: Batch Document Classification
    print("\n2. Testing Batch Document Classification...")
    profiler.run_test(
        "Batch Document Classification",
        batch_classify_document,
        duration=10,
        concurrency=3
    )

    # Test 3: Single Document Summarization
    print("\n3. Testing Single Document Summarization...")
    profiler.run_test(
        "Single Document Summarization",
        single_summarize_document,
        duration=10,
        concurrency=1
    )

    # Test 4: Batch Document Summarization
    print("\n4. Testing Batch Document Summarization...")
    profiler.run_test(
        "Batch Document Summarization",
        batch_summarize_document,
        duration=10,
        concurrency=2
    )

    # Print summary
    profiler.print_summary()

    # Save results
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    results_file = f"batch_comparison_results_{timestamp}.json"
    profiler.save_results(results_file)
    print(f"\nResults saved to: {results_file}")

    # Cleanup
    shutdown_all_processors()
    print("\nBatch processing comparison completed!")

if __name__ == "__main__":
    try:
        run_batch_comparison()
    except Exception as e:
        print(f"Error during batch comparison test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Ensure cleanup
        shutdown_all_processors()




