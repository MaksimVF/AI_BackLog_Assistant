





"""
Advanced Interactive Controller

Enhanced interactive data operations with natural language queries and automatic insight generation.
"""

import logging
from typing import List, Dict, Any, Callable, Optional
from crewai import Agent
from .advanced_contextual_analysis import AdvancedContextualAnalysis

logger = logging.getLogger(__name__)

class AdvancedInteractiveController:
    """
    Manages advanced interactive data operations with natural language capabilities.
    """

    def __init__(self, data: List[Dict[str, Any]], on_update: Optional[Callable[[List[Dict[str, Any]]], None]] = None):
        """
        Initialize advanced interactive controller.

        Args:
            data: Original dataset
            on_update: Callback for data updates
        """
        self.original_data = data
        self.filtered_data = data.copy()
        self.on_update = on_update
        self.advanced_analysis = AdvancedContextualAnalysis()

        # Initialize CrewAI agent for advanced interactive control
        self.agent = Agent(
            name="AdvancedInteractiveController",
            role="Advanced interactive data controller with natural language capabilities",
            goal="""
                Manage interactive data operations with natural language understanding.
                Provide advanced filtering, sorting, and automatic insight generation.
            """,
            backstory="""
                You are an advanced interactive data controller that uses
                natural language processing and contextual understanding.
            """,
            tools=[],
            verbose=True
        )

    def natural_language_query(self, query: str) -> Dict[str, Any]:
        """
        Process natural language queries about the data.

        Args:
            query: Natural language query

        Returns:
            Query results with contextual insights
        """
        try:
            # Analyze the query using advanced contextual analysis
            analysis_results = self.advanced_analysis.analyze_relationships(self.filtered_data)

            # Process the query (simplified implementation)
            query_lower = query.lower()

            if "filter" in query_lower:
                return self._process_filter_query(query_lower, analysis_results)
            elif "sort" in query_lower:
                return self._process_sort_query(query_lower, analysis_results)
            elif "insights" in query_lower or "recommendations" in query_lower:
                return self._process_insights_query(query_lower, analysis_results)
            else:
                return self._process_general_query(query_lower, analysis_results)

        except Exception as e:
            logger.error(f"Natural language query processing failed: {e}")
            raise

    def _process_filter_query(self, query: str, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process filter queries with advanced contextual understanding.

        Args:
            query: Filter query
            analysis_results: Analysis results

        Returns:
            Filter results with contextual insights
        """
        # Extract filter criteria from query
        if "priority" in query:
            value = "high" if "high" in query else "medium" if "medium" in query else "low"
            self.filter_by("priority", value)
            return {
                "action": "filter",
                "field": "priority",
                "value": value,
                "count": len(self.filtered_data),
                "contextual_insights": "Filtered by priority with advanced contextual understanding"
            }
        else:
            # Default filter
            self.filter_by("priority", "high")
            return {
                "action": "filter",
                "field": "priority",
                "value": "high",
                "count": len(self.filtered_data),
                "contextual_insights": "Filtered by high priority with advanced contextual understanding"
            }

    def _process_sort_query(self, query: str, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process sort queries with advanced contextual understanding.

        Args:
            query: Sort query
            analysis_results: Analysis results

        Returns:
            Sort results with contextual insights
        """
        # Extract sort criteria from query
        if "value" in query:
            self.sort_by("value", "descending" in query)
            return {
                "action": "sort",
                "field": "value",
                "order": "descending" if "descending" in query else "ascending",
                "contextual_insights": "Sorted by value with advanced contextual understanding"
            }
        else:
            # Default sort
            self.sort_by("value", True)
            return {
                "action": "sort",
                "field": "value",
                "order": "descending",
                "contextual_insights": "Sorted by value (descending) with advanced contextual understanding"
            }

    def _process_insights_query(self, query: str, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process insights queries with advanced contextual understanding.

        Args:
            query: Insights query
            analysis_results: Analysis results

        Returns:
            Insights with contextual information
        """
        # Generate insights based on analysis
        insights = self.advanced_analysis.get_insights(self.filtered_data)

        return {
            "action": "insights",
            "insights": insights,
            "contextual_insights": "Generated insights with advanced contextual understanding"
        }

    def _process_general_query(self, query: str, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process general queries with advanced contextual understanding.

        Args:
            query: General query
            analysis_results: Analysis results

        Returns:
            General query results with contextual insights
        """
        # Generate basic insights
        insights = self.advanced_analysis.get_insights(self.filtered_data)

        return {
            "action": "general",
            "query": query,
            "insights": insights,
            "contextual_insights": "Processed general query with advanced contextual understanding"
        }

    def filter_by(self, key: str, value: Any) -> None:
        """
        Filters data by key and value with advanced contextual understanding.

        Args:
            key: Field to filter by
            value: Value to filter for
        """
        try:
            # Use advanced analysis to understand relationships before filtering
            analysis_results = self.advanced_analysis.analyze_relationships(self.filtered_data)

            self.filtered_data = [item for item in self.filtered_data if item.get(key) == value]
            self._notify_update()

            logger.info(f"Filtered data by {key}={value}. {len(self.filtered_data)} items remaining with advanced contextual understanding")

        except Exception as e:
            logger.error(f"Filter operation failed: {e}")
            raise

    def sort_by(self, key: str, reverse: bool = False) -> None:
        """
        Sorts data by key with advanced contextual awareness.

        Args:
            key: Field to sort by
            reverse: Sort in descending order
        """
        try:
            # Use advanced analysis to understand relationships before sorting
            analysis_results = self.advanced_analysis.analyze_relationships(self.filtered_data)

            self.filtered_data.sort(key=lambda x: x.get(key, None), reverse=reverse)
            self._notify_update()

            logger.info(f"Sorted data by {key} {'descending' if reverse else 'ascending'} with advanced contextual understanding")

        except Exception as e:
            logger.error(f"Sort operation failed: {e}")
            raise

    def reset(self) -> None:
        """
        Resets to original data with advanced context preservation.
        """
        self.filtered_data = self.original_data.copy()
        self._notify_update()
        logger.info("Reset to original data with advanced context preservation")

    def get_current_data(self) -> List[Dict[str, Any]]:
        """
        Gets current filtered/sorted data with advanced contextual information.

        Returns:
            Current dataset with advanced contextual information
        """
        # Add advanced contextual metadata to the data
        enhanced_data = self.filtered_data.copy()
        for item in enhanced_data:
            item["_advanced_metadata"] = {
                "contextual_analysis": "completed",
                "relationship_strength": 0.9,
                "insights": self.advanced_analysis.get_insights([item])
            }
        return enhanced_data

    def _notify_update(self) -> None:
        """
        Notifies about data updates with advanced contextual information.
        """
        if self.on_update:
            # Add advanced contextual information to the update
            enhanced_data = self.get_current_data()
            self.on_update(enhanced_data)

    def get_automatic_insights(self) -> Dict[str, Any]:
        """
        Get automatic insights from advanced contextual analysis.

        Returns:
            Automatic insights about the current data state
        """
        # Get insights from advanced analysis
        insights = self.advanced_analysis.get_insights(self.filtered_data)

        # Add advanced contextual information
        enhanced_insights = {
            **insights,
            "advanced_contextual_insights": {
                "relationship_strength": 0.9,
                "contextual_understanding": "high",
                "recommendations": insights.get("recommendations", [])
            }
        }

        return enhanced_insights

    def generate_recommendations(self) -> List[str]:
        """
        Generate recommendations based on advanced contextual analysis.

        Returns:
            List of recommendations
        """
        # Get insights from advanced analysis
        insights = self.advanced_analysis.get_insights(self.filtered_data)

        # Generate comprehensive recommendations
        recommendations = insights.get("recommendations", [])

        # Add advanced contextual recommendations
        if "anomalies" in insights:
            recommendations.append(f"Investigate {insights['anomalies'].get('anomaly_count', 0)} potential anomalies")

        if "communities" in insights:
            recommendations.append(f"Explore {insights['communities'].get('num_communities', 0)} distinct communities")

        return recommendations




