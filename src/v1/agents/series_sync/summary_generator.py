















"""
SummaryGenerator for SeriesSync Agent

Generates human-readable summaries from data series, patterns, and relevant cases.
"""

from typing import List, Dict, Any

class SummaryGenerator:
    """
    Generates comprehensive summaries from analyzed data.
    """

    def __init__(self, summarization_model: Any = None):
        """
        Initialize with optional summarization model.

        :param summarization_model: Optional LLM or summarization model
        """
        self.model = summarization_model

    def generate_summary(
        self,
        data_series: List[Dict],
        patterns: Dict[str, Any],
        relevant_cases: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generates a comprehensive summary from data series, patterns, and relevant cases.

        :param data_series: Original data series
        :param patterns: Patterns detected by PatternRecognizer
        :param relevant_cases: Relevant cases found by CaseRetriever
        :return: Dictionary with summary text, recommendations, and bullet points
        """
        # Generate basic summary
        summary_text = self._generate_summary_text(data_series, patterns, relevant_cases)
        recommendations = self._generate_recommendations(patterns, relevant_cases)
        bullet_points = self._generate_bullet_points(data_series, patterns)

        return {
            "summary_text": summary_text,
            "recommendations": recommendations,
            "bullet_points": bullet_points
        }

    def _generate_summary_text(
        self,
        data_series: List[Dict],
        patterns: Dict[str, Any],
        relevant_cases: List[Dict[str, Any]]
    ) -> str:
        """Generates the main summary text."""
        summary = f"Analyzed {len(data_series)} events from {data_series[0]['timestamp']} to {data_series[-1]['timestamp']}.\n\n"

        # Add pattern information
        summary += "Key Patterns Detected:\n"
        for pattern in patterns.get("patterns_detected", []):
            summary += f"- {pattern}\n"

        # Add trend summary
        summary += f"\nTrend Summary:\n{patterns.get('trend_summary', 'No trends detected')}\n\n"

        # Add relevant cases
        if relevant_cases:
            summary += f"Found {len(relevant_cases)} relevant historical cases:\n"
            for i, case in enumerate(relevant_cases[:3], 1):  # Show top 3
                summary += f"{i}. {case.get('title', 'Untitled')} - {case.get('category', 'Unknown')}\n"
        else:
            summary += "No relevant historical cases found.\n"

        return summary

    def _generate_recommendations(
        self,
        patterns: Dict[str, Any],
        relevant_cases: List[Dict[str, Any]]
    ) -> List[str]:
        """Generates recommendations based on patterns and cases."""
        recommendations = []

        # Basic recommendations based on patterns
        if "frequent incidents" in str(patterns).lower():
            recommendations.append("Consider implementing preventive measures for frequent incidents.")

        if "high volume" in patterns.get("trend_summary", "").lower():
            recommendations.append("Monitor the high volume of events closely.")

        # Recommendations based on relevant cases
        if relevant_cases:
            recommendations.append("Review similar historical cases for potential solutions.")

        if not recommendations:
            recommendations.append("Continue monitoring the situation.")

        return recommendations

    def _generate_bullet_points(
        self,
        data_series: List[Dict],
        patterns: Dict[str, Any]
    ) -> List[str]:
        """Generates bullet points summarizing key information."""
        bullet_points = []

        # Add basic statistics
        bullet_points.append(f"Total events: {len(data_series)}")
        bullet_points.append(f"Time range: {data_series[0]['timestamp']} to {data_series[-1]['timestamp']}")

        # Add pattern information
        for pattern in patterns.get("patterns_detected", []):
            bullet_points.append(f"Pattern: {pattern}")

        # Add anomaly information
        if patterns.get("anomalies"):
            bullet_points.append(f"Anomalies detected: {len(patterns['anomalies'])}")

        return bullet_points

# Import needed for type hints
from datetime import datetime


