

# agents/reflection_agent/pipeline_aggregator.py

"""
Pipeline aggregator for ReflectionAgent that coordinates text processing, cleaning,
entity extraction, and routing to appropriate sub-agents.
"""

from typing import Dict, Any
from agents.reflection_agent.contextual_router import route_text, router
from agents.analyzers.text_cleaner import TextCleaner
from agents.analyzers.entity_extractor import EntityExtractor
from handlers.report_handler import ReportHandler

class PipelineAggregator:
    """
    Coordinates the processing pipeline for ReflectionAgent.

    Steps:
    1. Text cleaning
    2. Entity extraction
    3. Contextual routing
    """

    def __init__(self):
        """Initialize pipeline components."""
        self.text_cleaner = TextCleaner()
        self.entity_extractor = EntityExtractor()
        self.report_handler = ReportHandler()

    def process(self, text: str) -> Dict[str, Any]:
        """
        Process text through the entire pipeline.

        :param text: raw input text
        :return: dictionary with processing results
        """
        # Step 1: Clean the text
        cleaning_result = self.text_cleaner.clean(text)
        cleaned_text = cleaning_result.get("cleaned_text", text)

        # Step 2: Extract entities
        entities = self.entity_extractor.extract(cleaned_text)

        # Step 3: Route to appropriate sub-agent
        agent_name = route_text(cleaned_text)

        # Step 4: Process with specific handler if needed
        result = {
            "original_text": text,
            "cleaned_text": cleaned_text,
            "entities": entities,
            "agent_name": agent_name
        }

        # If it's a report, use the report handler
        if agent_name == "report_handler":
            # Use the text as document_text for the report handler
            self.report_handler.document_text = cleaned_text
            report_result = self.report_handler.run()
            result["report_data"] = report_result

        return result

    def process_batch(self, texts: list[str]) -> list[Dict[str, Any]]:
        """
        Process multiple texts through the pipeline.

        :param texts: list of raw input texts
        :return: list of processing results
        """
        return [self.process(text) for text in texts]

    def get_available_agents(self) -> list[str]:
        """
        Get list of available sub-agents for routing.

        :return: list of agent names
        """
        return router.list_route_names()

    def get_agent_description(self, agent_name: str) -> str:
        """
        Get description of a specific sub-agent.

        :param agent_name: name of the agent
        :return: description of the agent
        """
        from agents.reflection_agent.contextual_router import get_route_description
        return get_route_description(agent_name)

# Example usage
if __name__ == "__main__":
    # Create pipeline
    pipeline = PipelineAggregator()

    # Sample text - contract
    contract_text = """
    Настоящий договор аренды заключён между ООО "Ромашка" и ИП Иванов И.И.
    Сумма аренды: 50000 руб. в месяц. Срок: с 15.07.2023 по 15.07.2024.
    Контактный телефон: 8 (495) 123-45-67, email: contact@romashka.ru
    """

    # Sample text - report
    report_text = """
    Ежемесячный отчёт о продажах за январь 2023 года
    Общая выручка: 1 500 000 руб.
    Количество клиентов: 456
    Средний чек: 7 123 руб.

    | Продукт       | Количество | Сумма       |
    |---------------|------------|-------------|
    | Виджет A      | 120        | 300 000 руб.|
    | Виджет B      | 85         | 250 000 руб.|
    | Виджет C      | 150        | 400 000 руб.|
    """

    # Process contract text
    print("Processing Contract:")
    print("=" * 50)
    contract_result = pipeline.process(contract_text)
    print(f"Original Text: {contract_result['original_text'][:100]}...")
    print(f"Cleaned Text: {contract_result['cleaned_text'][:100]}...")
    print(f"Entities: {contract_result['entities']}")
    print(f"Agent Name: {contract_result['agent_name']}")
    print()

    # Process report text
    print("Processing Report:")
    print("=" * 50)
    report_result = pipeline.process(report_text)
    print(f"Original Text: {report_result['original_text'][:100]}...")
    print(f"Cleaned Text: {report_result['cleaned_text'][:100]}...")
    print(f"Entities: {report_result['entities']}")
    print(f"Agent Name: {report_result['agent_name']}")

    # If it's a report, show the report data
    if "report_data" in report_result:
        print("\nReport Data:")
        print(f"Report Type: {report_result['report_data']['subtype']}")
        print(f"Period: {report_result['report_data']['metadata'].get('period', 'unknown')}")
        print(f"Currency: {report_result['report_data']['metadata'].get('currency', 'unknown')}")
        print(f"Key Metrics: {report_result['report_data']['metadata'].get('key_metrics', {})}")
        print(f"Number of Tables: {len(report_result['report_data']['tables'])}")

    # Show available agents
    print(f"\nAvailable Agents: {pipeline.get_available_agents()}")

    # Show agent description
    for agent in pipeline.get_available_agents():
        print(f"{agent}: {pipeline.get_agent_description(agent)}")

