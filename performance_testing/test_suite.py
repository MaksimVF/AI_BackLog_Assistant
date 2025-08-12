



"""
AI BackLog Assistant Performance Test Suite

Comprehensive performance tests for key system components.
"""

import os
import sys
import time
import random
from performance_testing.performance_profiler import PerformanceProfiler
from agents.categorization.document_classifier_agent import DocumentClassifierAgent
from agents.summary.summary_agent import SummaryAgent
from utils.batch_processor import get_batch_processor, shutdown_all_processors

# Add sample data
SAMPLE_DOCUMENTS = [
    "Договор аренды недвижимости между ООО 'Ромашка' и ИП Иванов И.И.",
    "Акт выполненных работ по проекту 'Солнце' от 01.01.2023",
    "Счет на оплату №12345 от 15.05.2023 на сумму 10000 рублей",
    "Протокол собрания акционеров ООО 'Весна' от 10.03.2023",
    "Трудовой договор с сотрудником Петровым П.П.",
    "Устав организации 'Заря' версия 1.0",
    "Заявление на отпуск от сотрудника Сидорова С.С.",
    "Отчет о финансовых результатах за 2022 год",
    "Техническое задание на разработку программного обеспечения",
    "Коммерческое предложение для компании 'Небо'",
    "Счет-фактура №789 от 20.06.2023",
    "Платёжное поручение №123456 от 25.06.2023",
    "Справка о доходах физического лица",
    "Приказ о назначении директора",
    "Протокол заседания совета директоров",
    "Договор поставки оборудования",
    "Акт приема-передачи оборудования",
    "Счет на оплату коммунальных услуг",
    "Договор оказания услуг",
    "Акт выполненных работ по ремонту"
]

def generate_random_document():
    """Generate a random document from the sample pool"""
    return random.choice(SAMPLE_DOCUMENTS)

def test_document_classification():
    """Test document classification performance"""
    classifier = DocumentClassifierAgent()

    def classify_random_doc():
        """Classify a random document"""
        doc = generate_random_document()
        return classifier.classify(doc)

    return classify_random_doc

def test_document_classification_batch():
    """Test batch document classification performance"""
    # Ensure batch processor is running
    processor = get_batch_processor("classifier", batch_size=3, max_wait_time=1.0)

    def classify_random_doc_batch():
        """Classify a random document using batch processing"""
        doc = generate_random_document()
        return processor.submit({"text": doc}, lambda x: None)

    return classify_random_doc_batch

def test_document_summarization():
    """Test document summarization performance"""
    summarizer = SummaryAgent()

    def summarize_random_doc():
        """Summarize a random document"""
        doc = generate_random_document()
        return summarizer.generate_summary(doc)

    return summarize_random_doc

def test_document_summarization_batch():
    """Test batch document summarization performance"""
    # Ensure batch processor is running
    processor = get_batch_processor("summarizer", batch_size=2, max_wait_time=1.5)

    def summarize_random_doc_batch():
        """Summarize a random document using batch processing"""
        doc = generate_random_document()
        return processor.submit({"text": doc}, lambda x: None)

    return summarize_random_doc_batch

def test_llm_caching():
    """Test LLM caching performance"""
    from agents.llm_client import chat_completion

    system_prompt = "You are a helpful assistant."

    def llm_request():
        """Make an LLM request with caching"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "What is the capital of France?"}
        ]
        return chat_completion(messages)

    return llm_request

def run_full_test_suite():
    """Run the complete performance test suite"""
    print("Starting AI BackLog Assistant Performance Test Suite...")
    print("=" * 60)

    profiler = PerformanceProfiler()

    # Test 1: Document Classification (Single)
    print("\n1. Testing Document Classification (Single)...")
    profiler.run_test(
        "Document Classification (Single)",
        test_document_classification(),
        duration=10,
        concurrency=2
    )

    # Test 2: Document Classification (Batch)
    print("\n2. Testing Document Classification (Batch)...")
    profiler.run_test(
        "Document Classification (Batch)",
        test_document_classification_batch(),
        duration=10,
        concurrency=4
    )

    # Test 3: Document Summarization (Single)
    print("\n3. Testing Document Summarization (Single)...")
    profiler.run_test(
        "Document Summarization (Single)",
        test_document_summarization(),
        duration=10,
        concurrency=1
    )

    # Test 4: Document Summarization (Batch)
    print("\n4. Testing Document Summarization (Batch)...")
    profiler.run_test(
        "Document Summarization (Batch)",
        test_document_summarization_batch(),
        duration=10,
        concurrency=3
    )

    # Test 5: LLM Caching
    print("\n5. Testing LLM Caching Performance...")
    profiler.run_test(
        "LLM Caching",
        test_llm_caching(),
        duration=10,
        concurrency=5
    )

    # Print summary
    profiler.print_summary()

    # Save results
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    results_file = f"performance_results_{timestamp}.json"
    profiler.save_results(results_file)
    print(f"\nResults saved to: {results_file}")

    # Cleanup
    shutdown_all_processors()
    print("\nPerformance test suite completed!")

if __name__ == "__main__":
    try:
        run_full_test_suite()
    except Exception as e:
        print(f"Error during performance testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Ensure cleanup
        from utils.batch_processor import shutdown_all_processors
        shutdown_all_processors()



