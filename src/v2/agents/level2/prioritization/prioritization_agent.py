



"""
Prioritization Agent for Level 2 Processing
"""

from crewai import Agent

class PrioritizationAgent:
    """Prioritizes documents based on content and metadata"""

    def __init__(self):
        # Initialize CrewAI agent
        self.agent = Agent(
            name="PrioritizationAgent",
            role="Агент приоритизации документов",
            goal="""
                Определить приоритет обработки документов на основе их содержания,
                классификации и метаданных.
            """,
            backstory="""
                Ты — агент, отвечающий за определение приоритетов обработки.
                Используешь алгоритмы и правила для оценки важности документов.
            """,
            tools=[],
            verbose=True
        )

    def prioritize(self, input_data: dict) -> dict:
        """
        Prioritize document processing

        Args:
            input_data: Data from Level 1 and categorization

        Returns:
            Data with added prioritization information
        """
        # Process using CrewAI agent
        result = self.agent.process(input_data)

        # Add prioritization to data
        prioritized_data = {
            **input_data,
            "prioritization": {
                "priority_level": result.get("priority_level", "medium"),
                "priority_score": result.get("priority_score", 0.5),
                "reason": result.get("reason", "default prioritization")
            }
        }

        return prioritized_data


