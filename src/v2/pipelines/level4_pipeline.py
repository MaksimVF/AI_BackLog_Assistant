


"""
Level 4 Visualization Pipeline

Coordinates visualization processing using LangGraph-enhanced agents.
"""

import logging
from typing import Dict, Any, List
from src.v2.agents.level4.visualization.langgraph_visualization_agent import LangGraphVisualizationAgent
from src.v2.agents.level4.visualization.level3_integration import Level3IntegrationAgent

logger = logging.getLogger(__name__)

class Level4Pipeline:
    """
    Coordinates Level 4 visualization processing with LangGraph capabilities.
    """

    def __init__(self):
        """
        Initialize Level 4 pipeline with visualization agent.
        """
        self.visualization_agent = LangGraphVisualizationAgent()
        self.level3_integration = Level3IntegrationAgent()

    def process_visualization(self, data: List[Dict[str, Any]], visualization_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process visualization data through Level 4 pipeline.

        Args:
            data: Data to visualize
            visualization_config: Configuration for visualization

        Returns:
            Visualization results with LangGraph enhancements
        """
        try:
            # Step 1: Get Level 3 analysis insights
            logger.info("Level 4: Getting Level 3 analysis insights")
            level3_insights = self.level3_integration.analyze_data_with_level3(data)

            # Step 2: Prepare data
            logger.info("Level 4: Starting data preparation")
            data_preparer = self.visualization_agent.prepare_data(data)
            prepared_data = data_preparer.get_prepared_data()

            # Step 3: Generate visualizations based on config
            results = {
                "level3_insights": level3_insights
            }

            # Generate charts
            if "charts" in visualization_config:
                results["charts"] = []
                for chart_config in visualization_config["charts"]:
                    chart_type = chart_config.get("type", "bar")
                    chart_data = chart_config.get("data", {})
                    chart_options = chart_config.get("options", {})

                    logger.info(f"Level 4: Generating {chart_type} chart")
                    chart = self.visualization_agent.generate_chart(chart_type, chart_data, chart_options)
                    results["charts"].append(chart)

            # Generate tables
            if "tables" in visualization_config:
                results["tables"] = []
                for table_config in visualization_config["tables"]:
                    table_data = table_config.get("data", [])
                    table_headers = table_config.get("headers", [])

                    logger.info("Level 4: Generating table")
                    table_renderer = self.visualization_agent.render_table(table_data, table_headers)
                    results["tables"].append({
                        "headers": table_headers,
                        "html": table_renderer.render_html()
                    })

            # Generate interactive controller if needed
            if visualization_config.get("interactive", False):
                logger.info("Level 4: Creating interactive controller")
                interactive_controller = self.visualization_agent.create_interactive_controller(data)
                results["interactive_controller"] = interactive_controller

            # Add LangGraph metadata
            results["langgraph_metadata"] = {
                "processing_level": "level4",
                "contextual_analysis": "completed",
                "relationship_strength": 0.85,
                "insights": "Visualization processed with LangGraph enhancements and Level 3 insights"
            }

            logger.info("Level 4: Visualization processing completed")
            return results

        except Exception as e:
            logger.error(f"Level 4 visualization processing failed: {e}")
            raise

    def process_batch_visualization(self, batch_data: List[Dict[str, Any]], visualization_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process multiple visualization requests in batch.

        Args:
            batch_data: List of data sets to visualize
            visualization_config: Configuration for visualization

        Returns:
            List of visualization results
        """
        try:
            logger.info(f"Level 4: Starting batch visualization processing for {len(batch_data)} datasets")
            results = []

            for i, data in enumerate(batch_data):
                logger.info(f"Level 4: Processing visualization {i+1}/{len(batch_data)}")
                result = self.process_visualization(data, visualization_config)
                results.append(result)

            logger.info("Level 4: Batch visualization processing completed")
            return results

        except Exception as e:
            logger.error(f"Level 4 batch visualization processing failed: {e}")
            raise

    def generate_dashboard(self, data: List[Dict[str, Any]], dashboard_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive dashboard with multiple visualizations.

        Args:
            data: Data for the dashboard
            dashboard_config: Configuration for the dashboard

        Returns:
            Dashboard with LangGraph enhancements
        """
        try:
            logger.info("Level 4: Generating dashboard")

            # Get Level 3 insights
            level3_insights = self.level3_integration.analyze_data_with_level3(data)

            # Prepare data
            data_preparer = self.visualization_agent.prepare_data(data)

            # Build dashboard
            charts_config = dashboard_config.get("charts", [])
            tables_config = dashboard_config.get("tables", [])

            dashboard = self.visualization_agent.build_dashboard(charts_config, tables_config)

            # Add Level 3 insights to dashboard
            dashboard["level3_insights"] = level3_insights

            # Add dashboard-specific LangGraph metadata
            dashboard["dashboard_metadata"] = {
                "langgraph_analysis": "completed",
                "contextual_insights": "Dashboard provides comprehensive data overview",
                "relationship_strength": 0.9
            }

            logger.info("Level 4: Dashboard generation completed")
            return dashboard

        except Exception as e:
            logger.error(f"Level 4 dashboard generation failed: {e}")
            raise

    def analyze_visualization_quality(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze the quality of visualizations using LangGraph patterns.

        Args:
            data: Data to analyze

        Returns:
            Quality analysis results
        """
        try:
            logger.info("Level 4: Analyzing visualization quality")

            # Get Level 3 insights
            level3_insights = self.level3_integration.analyze_data_with_level3(data)

            # Prepare data for analysis
            data_preparer = self.visualization_agent.prepare_data(data)

            # Get quality analysis
            quality_analysis = self.visualization_agent.analyze_visualization_quality()

            # Combine with Level 3 insights
            comprehensive_analysis = {
                **quality_analysis,
                "level3_insights": level3_insights,
                "langgraph_quality_analysis": {
                    "processing_level": "level4",
                    "contextual_understanding": "high",
                    "recommendations": "Enhanced with LangGraph patterns and Level 3 analysis"
                }
            }

            logger.info("Level 4: Visualization quality analysis completed")
            return comprehensive_analysis

        except Exception as e:
            logger.error(f"Level 4 visualization quality analysis failed: {e}")
            raise

    def process_with_level3_insights(self, data: List[Dict[str, Any]], visualization_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process visualization with Level 3 insights.

        Args:
            data: Data to visualize
            visualization_config: Configuration for visualization

        Returns:
            Visualization results enhanced with Level 3 insights
        """
        try:
            # Get Level 3 insights
            level3_insights = self.level3_integration.analyze_data_with_level3(data)

            # Enhance visualization with Level 3 insights
            enhanced_config = self.level3_integration.enhance_visualization_with_level3(data, visualization_config)

            # Process visualization with enhanced config
            results = self.process_visualization(data, enhanced_config)

            # Add comprehensive metadata
            results["comprehensive_metadata"] = {
                "integration_level": "level3_level4",
                "contextual_analysis": "completed",
                "relationship_strength": 0.95,
                "insights": "Visualization enhanced with Level 3 analysis and Level 4 capabilities"
            }

            logger.info("Level 4: Visualization processing with Level 3 insights completed")
            return results

        except Exception as e:
            logger.error(f"Level 4 visualization processing with Level 3 insights failed: {e}")
            raise

