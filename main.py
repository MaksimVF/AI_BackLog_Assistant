from agents.reflection_agent import ReflectionAgent, ReflectionInput
from memory.weaviate_client import WeaviateMemory
from schemas import VideoData, AudioData, ImageData, DocumentData, TextData

def main():
    # Initialize components
    memory = WeaviateMemory()
    reflection_agent = ReflectionAgent(memory=memory)

    # Example usage
    print("Добро пожаловать в мультиагентную систему!")

    # Create sample text data for reflection agent (in Russian)
    sample_text = """
    Я хочу улучшить свою бизнес-стратегию и оптимизировать маркетинговые кампании.
    Нам нужно достичь лучшего вовлечения клиентов и развить новые каналы продаж.
    Цель - трансформировать нашу бизнес-модель, чтобы быть более конкурентоспособными на рынке.
    """

    # Process with reflection agent
    input_data = ReflectionInput(
        content=sample_text,
        metadata={
            "source": "user_input",
            "lang": "ru",
            "user_id": "1234",
            "timestamp": "2025-07-29T12:00:00Z"
        }
    )

    result = reflection_agent.execute(input_data)

    print("\nРезультаты анализа Reflection Agent:")
    print(f"Контекст: {result.context}")
    print(f"Теги домена: {', '.join(result.domain_tags)}")
    print(f"Рекомендованные агенты: {', '.join(result.recommended_agents)}")
    print(f"Обоснование: {result.reasoning}")

    if result.similarity_case_id:
        print(f"Найден похожий кейс: {result.similarity_case_id}")
    else:
        print("Похожие кейсы не найдены.")

    print("\nОбработка завершена!")

if __name__ == "__main__":
    main()
