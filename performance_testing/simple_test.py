



"""
Simple Performance Test

Basic performance test without external dependencies.
"""

import time
import random
from performance_testing.performance_profiler import PerformanceProfiler

# Simple mock functions to simulate agent behavior
def mock_classify_document(doc_text):
    """Mock document classification"""
    # Simulate processing time
    time.sleep(0.1 + random.random() * 0.1)
    if "договор" in doc_text.lower():
        return "contract"
    elif "счет" in doc_text.lower():
        return "invoice"
    else:
        return "other"

def mock_summarize_document(doc_text):
    """Mock document summarization"""
    # Simulate processing time
    time.sleep(0.2 + random.random() * 0.1)
    return {
        "summary": f"Summary of: {doc_text[:50]}...",
        "keypoints": ["Point 1", "Point 2", "Point 3"],
        "insights": ["Insight 1"]
    }

def mock_llm_request(prompt):
    """Mock LLM request"""
    # Simulate processing time
    time.sleep(0.15 + random.random() * 0.1)
    return f"Response to: {prompt[:30]}..."

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

def run_simple_performance_tests():
    """Run simple performance tests"""
    print("Running Simple Performance Tests...")
    print("=" * 50)

    profiler = PerformanceProfiler()

    # Test 1: Document Classification
    print("\n1. Testing Document Classification...")
    profiler.run_test(
        "Document Classification",
        mock_classify_document,
        duration=5,
        concurrency=2,
        doc_text="Договор аренды недвижимости"
    )

    # Test 2: Document Summarization
    print("\n2. Testing Document Summarization...")
    profiler.run_test(
        "Document Summarization",
        mock_summarize_document,
        duration=5,
        concurrency=1,
        doc_text="Счет на оплату №12345"
    )

    # Test 3: LLM Requests
    print("\n3. Testing LLM Requests...")
    profiler.run_test(
        "LLM Requests",
        mock_llm_request,
        duration=5,
        concurrency=3,
        prompt="What is the capital of France?"
    )

    # Print summary
    profiler.print_summary()

    # Save results
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    results_file = f"simple_performance_results_{timestamp}.json"
    profiler.save_results(results_file)
    print(f"\nResults saved to: {results_file}")

    print("\nSimple performance tests completed!")

if __name__ == "__main__":
    run_simple_performance_tests()



