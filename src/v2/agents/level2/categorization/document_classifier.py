


"""
Document Classifier Agent for Level 2 Processing
"""

from crewai import Agent

class DocumentClassifierAgent:
    """Classifies documents into categories"""

    def __init__(self):
        # Initialize CrewAI agent
        self.agent = Agent(
            name="DocumentClassifierAgent",
            role="Агент классификации документов",
            goal="""
                Классифицировать документы по категориям на основе их содержания.
                Определить основную тему, домен и тип документа.
            """,
            backstory="""
                Ты — агент, отвечающий за анализ документов и их классификацию.
                Используешь NLP и машинное обучение для определения категорий.
            """,
            tools=[],
            verbose=True
        )

    def classify(self, input_data: dict) -> dict:
        """
        Classify document into categories

        Args:
            input_data: Data from Level 1 processing

        Returns:
            Data with added classification information
        """
        # Process using CrewAI agent
        result = self.agent.process(input_data)

        # Add classification to data
        classified_data = {
            **input_data,
            "classification": {
                "category": result.get("category", "unknown"),
                "domain": result.get("domain", "unknown"),
                "confidence": result.get("confidence", 0.7)
            }
        }

        return classified_data

