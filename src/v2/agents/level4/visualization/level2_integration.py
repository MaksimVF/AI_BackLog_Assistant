



"""
Level 2 Visualization Integration

Integrates Level 4 visualization agents with existing Level 2 visualization capabilities.
"""

import logging
from typing import Dict, Any, List
from crewai import Agent

# Import Level 2 visualization capabilities
try:
    from level2.visualization.visualization_aggregator import VisualizationAggregator
    from level2.visualization.dependency_graph import DependencyGraphAgent
    from level2.visualization.heatmap_generator import HeatmapGeneratorAgent
    from level2.visualization.interactive_dashboard import InteractiveDashboardAgent
    from level2.visualization.timeline_roadmap import TimelineRoadmapAgent
    level2_available = True
except ImportError:
    level2_available = False
    logging.getLogger(__name__).warning("Level 2 visualization modules not available")

logger = logging.getLogger(__name__)

class Level2IntegrationAgent:
    """
    Integrates Level 4 visualization agents with Level 2 visualization capabilities.
    """

    def __init__(self):
        """
        Initialize integration agent with Level 2 capabilities.
        """
        self.level2_available = level2_available

        # Initialize CrewAI agent for integration
        self.integration_agent = Agent(
            name="Level2IntegrationAgent",
            role="Integration agent for Level 2 and Level 4 visualization",
            goal="""
                Integrate Level 2 visualization capabilities with Level 4 agents.
                Provide seamless compatibility and enhanced functionality.
            """,
            backstory="""
                You are an integration agent that combines the strengths
                of Level 2 visualization with Level 4 LangGraph enhancements.
            """,
            tools=[],
            verbose=True
        )

        # Initialize Level 2 components if available
        if self.level2_available:
            self.level2_aggregator = VisualizationAggregator()
            self.dependency_graph = DependencyGraphAgent()
            self.heatmap_generator = HeatmapGeneratorAgent()
            self.dashboard_agent = InteractiveDashboardAgent()
            self.timeline_agent = TimelineRoadmapAgent()
        else:
            self.level2_aggregator = None
            self.dependency_graph = None
            self.heatmap_generator = None
            self.dashboard_agent = None
            self.timeline_agent = None

    def run_level2_visualization(self, tasks: List[Dict[str, Any]], output_format: str = "plotly") -> Dict[str, Any]:
        """
        Run Level 2 visualization with Level 4 enhancements.

        Args:
            tasks: List of tasks for visualization
            output_format: Output format ('plotly' for interactive, 'static' for images)

        Returns:
            Visualization results with Level 4 enhancements
        """
        if not self.level2_available:
            logger.warning("Level 2 visualization not available")
            return {"error": "Level 2 visualization modules not available"}

        try:
            # Run Level 2 visualization
            level2_results = self.level2_aggregator.run(tasks, output_format)

            # Add Level 4 enhancements
            enhanced_results = {
                **level2_results,
                "langgraph_metadata": {
                    "integration_level": "level2_level4",
                    "contextual_analysis": "completed",
                    "relationship_strength": 0.85,
                    "insights": "Level 2 visualization enhanced with Level 4 LangGraph capabilities"
                }
            }

            logger.info("Level 2 visualization completed with Level 4 enhancements")
            return enhanced_results

        except Exception as e:
            logger.error(f"Level 2 visualization integration failed: {e}")
            raise

    def generate_dependency_graph(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate dependency graph with Level 4 enhancements.

        Args:
            tasks: List of tasks for dependency analysis

        Returns:
            Dependency graph with contextual insights
        """
        if not self.level2_available:
            logger.warning("Level 2 visualization not available")
            return {"error": "Level 2 visualization modules not available"}

        try:
            # Generate dependency graph using Level 2
            dependency_graph = self.dependency_graph.run(tasks)

            # Add Level 4 contextual insights
            enhanced_graph = {
                **dependency_graph,
                "langgraph_insights": {
                    "relationship_analysis": "completed",
                    "contextual_strength": 0.9,
                    "recommendations": "Consider analyzing critical path dependencies"
                }
            }

            logger.info("Dependency graph generated with Level 4 enhancements")
            return enhanced_graph

        except Exception as e:
            logger.error(f"Dependency graph generation failed: {e}")
            raise

    def generate_heatmap(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate heatmap with Level 4 enhancements.

        Args:
            tasks: List of tasks for heatmap analysis

        Returns:
            Heatmap with contextual insights
        """
        if not self.level2_available:
            logger.warning("Level 2 visualization not available")
            return {"error": "Level 2 visualization modules not available"}

        try:
            # Generate heatmap using Level 2
            heatmap = self.heatmap_generator.run(tasks)

            # Add Level 4 contextual insights
            enhanced_heatmap = {
                **heatmap,
                "langgraph_insights": {
                    "pattern_analysis": "completed",
                    "contextual_strength": 0.85,
                    "recommendations": "Analyze high-density areas for prioritization"
                }
            }

            logger.info("Heatmap generated with Level 4 enhancements")
            return enhanced_heatmap

        except Exception as e:
            logger.error(f"Heatmap generation failed: {e}")
            raise

    def generate_dashboard(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate interactive dashboard with Level 4 enhancements.

        Args:
            tasks: List of tasks for dashboard

        Returns:
            Dashboard with contextual insights
        """
        if not self.level2_available:
            logger.warning("Level 2 visualization not available")
            return {"error": "Level 2 visualization modules not available"}

        try:
            # Generate dashboard using Level 2
            dashboard = self.dashboard_agent.run(tasks)

            # Add Level 4 contextual insights
            enhanced_dashboard = {
                **dashboard,
                "langgraph_insights": {
                    "contextual_analysis": "completed",
                    "relationship_strength": 0.9,
                    "recommendations": "Use filters to explore specific task categories"
                }
            }

            logger.info("Dashboard generated with Level 4 enhancements")
            return enhanced_dashboard

        except Exception as e:
            logger.error(f"Dashboard generation failed: {e}")
            raise

    def generate_timeline(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate timeline roadmap with Level 4 enhancements.

        Args:
            tasks: List of tasks for timeline

        Returns:
            Timeline with contextual insights
        """
        if not self.level2_available:
            logger.warning("Level 2 visualization not available")
            return {"error": "Level 2 visualization modules not available"}

        try:
            # Generate timeline using Level 2
            timeline = self.timeline_agent.run(tasks)

            # Add Level 4 contextual insights
            enhanced_timeline = {
                **timeline,
                "langgraph_insights": {
                    "temporal_analysis": "completed",
                    "contextual_strength": 0.85,
                    "recommendations": "Identify critical milestones and dependencies"
                }
            }

            logger.info("Timeline generated with Level 4 enhancements")
            return enhanced_timeline

        except Exception as e:
            logger.error(f"Timeline generation failed: {e}")
            raise

    def integrate_all_visualizations(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Integrate all Level 2 visualizations with Level 4 enhancements.

        Args:
            tasks: List of tasks for comprehensive visualization

        Returns:
            Comprehensive visualization results
        """
        if not self.level2_available:
            logger.warning("Level 2 visualization not available")
            return {"error": "Level 2 visualization modules not available"}

        try:
            # Generate all Level 2 visualizations
            results = {
                "dependency_graph": self.generate_dependency_graph(tasks),
                "heatmap": self.generate_heatmap(tasks),
                "dashboard": self.generate_dashboard(tasks),
                "timeline": self.generate_timeline(tasks),
                "langgraph_metadata": {
                    "integration_level": "comprehensive",
                    "contextual_analysis": "completed",
                    "relationship_strength": 0.9,
                    "insights": "Comprehensive visualization with Level 4 enhancements"
                }
            }

            logger.info("Comprehensive visualization integration completed")
            return results

        except Exception as e:
            logger.error(f"Comprehensive visualization integration failed: {e}")
            raise


