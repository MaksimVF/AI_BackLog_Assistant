




"""
Main Summary Agent with Batch Processing Support
"""

from agents.summary.summary_extractor_agent import SummaryExtractorAgent
from agents.summary.keypoint_compressor_agent import KeypointCompressorAgent
from agents.summary.insight_generator_agent import InsightGeneratorAgent
from utils.batch_decorator import batch_processing

class SummaryAgent:
    """
    Агрегатор для генерации полного резюме документа:
    краткое содержание, ключевые пункты, аналитика, финальный отчёт.
    """

    def __init__(self):
        self.summary_extractor = SummaryExtractorAgent()
        self.keypoint_compressor = KeypointCompressorAgent()
        self.insight_generator = InsightGeneratorAgent()

    @batch_processing(agent_type="summarizer", batch_size=2, max_wait_time=1.5)
    def generate_summary(self, document_text: str) -> dict:
        """
        Generates a complete summary of the document.

        Args:
            document_text: The text of the document to summarize

        Returns:
            Dictionary containing all summary components
        """
        # Extract main content
        summary = self.summary_extractor.extract_summary(document_text)

        # Compress to keypoints
        keypoints = self.keypoint_compressor.compress_to_keypoints(summary)

        # Generate insights
        insights = self.insight_generator.generate_insights(keypoints)

        return {
            "summary": summary,
            "keypoints": keypoints,
            "insights": insights
        }

    def generate_formatted_summary(self, document_text: str) -> str:
        """
        Generates a formatted summary report.

        Args:
            document_text: The text of the document to summarize

        Returns:
            Formatted summary string
        """
        summary_data = self.generate_summary(document_text)

        # Format the summary report
        report = (
            "=== Сводка документа ===\n\n"
            f"Основное содержание:\n{summary_data['summary']}\n\n"
            "Ключевые пункты:\n"
        )

        for i, point in enumerate(summary_data['keypoints'], 1):
            report += f"{i}. {point}\n"

        report += f"\nАналитические выводы:\n{summary_data['insights']}"

        return report




