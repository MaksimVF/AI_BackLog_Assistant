



from agents.contextualization_agent.contextualizer_core import ContextualizerCore

def test_contextualization_agent():
    """Test the ContextualizationAgent with a sample document."""

    # Initialize the contextualizer
    contextualizer = ContextualizerCore()

    # Sample document text
    document_text = """
    Договор № 345/2023 от 01.07.2023
    между ООО «Пример» и ИП Иванов

    1. Предмет договора
    ООО «Пример» обязуется поставить товары, а ИП Иванов обязуется принять и оплатить их.

    2. Сроки поставки
    Поставка должна быть осуществлена в течение 30 дней с момента подписания договора.

    3. Цена и порядок расчетов
    Общая стоимость товаров составляет 120 000,00 руб. Оплата производится в течение 5 дней после поставки.
    """

    # Process the document
    print("Processing document...")
    context = contextualizer.process_document(document_text)

    # Display results
    print("\n=== Document Context ===")
    print(f"Chunks: {len(context['chunks'])}")
    print(f"Knowledge Graph: {context['knowledge_graph']}")
    print(f"References: {len(context['references'])}")
    print(f"Clusters: {len(context['clusters'])}")

    # Test context retrieval
    print("\n=== Context Retrieval ===")
    query = "договор поставки"
    results = contextualizer.get_context_for_query(query)
    print(f"Query: '{query}'")
    print(f"Found {len(results)} relevant contexts:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result.get('text', '')[:100]}...")

    # Test memory clearing
    print("\n=== Memory Clearing ===")
    contextualizer.clear_context_memory()
    results_after_clear = contextualizer.get_context_for_query(query)
    print(f"After clearing memory, found {len(results_after_clear)} contexts")

if __name__ == "__main__":
    test_contextualization_agent()



