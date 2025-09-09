















"""
SeriesSync Agent

Main agent for aggregating, analyzing serial data, and generating summaries.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from agents.series_sync.data_series_collector import DataSeriesCollector
from agents.series_sync.pattern_recognizer import PatternRecognizer
from agents.series_sync.case_retriever import CaseRetriever
from agents.series_sync.summary_generator import SummaryGenerator

class SeriesSyncAgent:
    """
    SeriesSync Agent integrates multiple sub-agents to analyze event data and generate insights.

    Components:
    - DataSeriesCollector: Aggregates events based on time window and filters
    - PatternRecognizer: Detects patterns, trends, and anomalies
    - CaseRetriever: Finds relevant historical cases
    - SummaryGenerator: Creates comprehensive summaries
    """

    def __init__(
        self,
        event_log: List[Dict[str, Any]],
        case_database: List[Dict[str, Any]],
        summarization_model: Any = None,
        pattern_model: Any = None
    ):
        """
        Initialize SeriesSync Agent with all components.

        :param event_log: List of event dictionaries
        :param case_database: List of historical case dictionaries
        :param summarization_model: Optional LLM for summarization
        :param pattern_model: Optional ML model for pattern detection
        """
        self.data_collector = DataSeriesCollector(event_log)
        self.pattern_recognizer = PatternRecognizer(pattern_model)
        self.case_retriever = CaseRetriever(case_database)
        self.summary_generator = SummaryGenerator(summarization_model)

    def run(
        self,
        time_window_start: str,
        time_window_end: str,
        filters: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Main method to analyze event data and generate summary.

        :param time_window_start: Start date in 'YYYY-MM-DD' format
        :param time_window_end: End date in 'YYYY-MM-DD' format
        :param filters: Optional filters for data collection
        :param context: Optional context for case retrieval
        :return: Comprehensive analysis report
        """
        # Step 1: Collect data series
        data_series = self.data_collector.collect(
            time_window_start=time_window_start,
            time_window_end=time_window_end,
            filters=filters
        )

        # Step 2: Recognize patterns
        patterns = self.pattern_recognizer.recognize_patterns(data_series)

        # Step 3: Retrieve relevant cases
        if context is None:
            context = {}  # Default empty context
        relevant_cases = self.case_retriever.find_similar_cases(
            patterns=patterns,
            context=context
        )

        # Step 4: Generate summary
        summary = self.summary_generator.generate_summary(
            data_series=data_series,
            patterns=patterns,
            relevant_cases=relevant_cases
        )

        return {
            "data_series": data_series,
            "patterns": patterns,
            "relevant_cases": relevant_cases,
            "summary": summary
        }

    def generate_formatted_report(self, analysis_result: Dict[str, Any]) -> str:
        """
        Generates a formatted text report from analysis results.

        :param analysis_result: Result from run() method
        :return: Formatted text report
        """
        summary = analysis_result["summary"]
        patterns = analysis_result["patterns"]
        relevant_cases = analysis_result["relevant_cases"]

        report = "=== SeriesSync Analysis Report ===\n\n"

        # Add summary
        report += "SUMMARY:\n"
        report += summary["summary_text"] + "\n\n"

        # Add recommendations
        report += "RECOMMENDATIONS:\n"
        for i, rec in enumerate(summary["recommendations"], 1):
            report += f"{i}. {rec}\n"

        # Add bullet points
        report += "\nKEY POINTS:\n"
        for point in summary["bullet_points"]:
            report += f"- {point}\n"

        # Add relevant cases
        if relevant_cases:
            report += "\nRELEVANT HISTORICAL CASES:\n"
            for i, case in enumerate(relevant_cases[:3], 1):  # Show top 3
                report += f"{i}. {case.get('title', 'Untitled')} ({case.get('category', 'Unknown')})\n"
                report += f"   Description: {case.get('description', 'No description')}\n"

        return report



