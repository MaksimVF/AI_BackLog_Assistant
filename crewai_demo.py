from crewai import Agent, Task, Crew
from agents.reflection_agent import ReflectionAgent
import json

def main():
    # Create our ReflectionAgent with CrewAI integration
    reflection_agent = ReflectionAgent()

    # Create CrewAI Task
    reflection_task = Task(
        description="Проанализируй предоставленный текст и определи, какие агенты нужны для его последующей обработки.",
        expected_output="JSON с ключами: context, domain_tags, recommended_agents, reasoning",
        agent=reflection_agent
    )

    # Create Crew with our agent and task
    crew = Crew(
        agents=[reflection_agent],
        tasks=[reflection_task],
        verbose=True
    )

    # Sample input data
    sample_text = """
    Я хочу улучшить свою бизнес-стратегию и оптимизировать маркетинговые кампании.
    Нам нужно достичь лучшего вовлечения клиентов и развить новые каналы продаж.
    Цель - трансформировать нашу бизнес-модель, чтобы быть более конкурентоспособными на рынке.
    """

    # Prepare input data
    input_data = {
        "content": sample_text,
        "metadata": {
            "source": "user_input",
            "lang": "ru",
            "user_id": "1234",
            "timestamp": "2025-07-29T12:00:00Z"
        }
    }

    print("Запуск CrewAI с ReflectionAgent...")
    print("Входные данные:", json.dumps(input_data, ensure_ascii=False, indent=2))

    # Execute the task
    result = crew.execute_task(
        task=reflection_task,
        input_data=json.dumps(input_data, ensure_ascii=False)
    )

    print("\nРезультаты анализа:")
    if isinstance(result, str):
        # Parse JSON result
        try:
            result_dict = json.loads(result)
            print(json.dumps(result_dict, ensure_ascii=False, indent=2))
        except:
            print(result)
    else:
        print(result)

if __name__ == "__main__":
    main()
