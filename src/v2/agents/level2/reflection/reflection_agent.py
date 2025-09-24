




"""
Reflection Agent for Level 2 Processing
"""

from crewai import Agent

class ReflectionAgent:
    """Performs reflection analysis on documents"""

    def __init__(self):
        # Initialize CrewAI agent
        self.agent = Agent(
            name="ReflectionAgent",
            role="Агент рефлексии и анализа документов",
            goal="""
                Провести анализ документов для выявления проблем, противоречий
                и областей для улучшения.
            """,
            backstory="""
                Ты — агент, отвечающий за критический анализ документов.
                Используешь NLP и логический анализ для выявления проблем.
            """,
            tools=[],
            verbose=True
        )

    def analyze(self, input_data: dict) -> dict:
        """
        Perform reflection analysis on document

        Args:
            input_data: Data from Level 1, categorization, and prioritization

        Returns:
            Data with added reflection analysis
        """
        # Process using CrewAI agent
        result = self.agent.process(input_data)

        # Add reflection analysis to data
        analyzed_data = {
            **input_data,
            "reflection": {
                "issues": result.get("issues", []),
                "contradictions": result.get("contradictions", []),
                "improvement_areas": result.get("improvement_areas", []),
                "quality_score": result.get("quality_score", 0.7)
            }
        }

        return analyzed_data



