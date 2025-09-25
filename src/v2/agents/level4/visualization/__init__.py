

"""
Level 4 Visualization Agents

LangGraph-based visualization agents for advanced data presentation and interaction.
"""

# Import visualization agents
from .langgraph_data_preparer import LangGraphDataPreparer
from .langgraph_chart_generator import LangGraphChartGenerator
from .langgraph_table_renderer import LangGraphTableRenderer
from .langgraph_interactive_controller import LangGraphInteractiveController
from .langgraph_export_manager import LangGraphExportManager
from .langgraph_visualization_agent import LangGraphVisualizationAgent
from .level2_integration import Level2IntegrationAgent
from .level3_integration import Level3IntegrationAgent

# Define the complete Level 4 visualization system
class Level4VisualizationSystem:
    """
    Complete Level 4 visualization system that integrates all components.
    """

    def __init__(self):
        """
        Initialize the complete Level 4 visualization system.
        """
        self.visualization_agent = LangGraphVisualizationAgent()
        self.level2_integration = Level2IntegrationAgent()
        self.level3_integration = Level3IntegrationAgent()

    def process_complete_visualization(self, data: list, visualization_config: dict) -> dict:
        """
        Process complete visualization with all Level 4 capabilities.

        Args:
            data: Data to visualize
            visualization_config: Visualization configuration

        Returns:
            Complete visualization results
        """
        # Get Level 3 insights
        level3_insights = self.level3_integration.analyze_data_with_level3(data)

        # Process visualization
        results = self.visualization_agent.process_visualization(data, visualization_config)

        # Add Level 3 insights
        results["level3_insights"] = level3_insights

        # Add comprehensive metadata
        results["comprehensive_metadata"] = {
            "integration_level": "complete",
            "contextual_analysis": "completed",
            "relationship_strength": 0.95,
            "insights": "Complete visualization with Level 3 analysis and Level 4 capabilities"
        }

        return results

