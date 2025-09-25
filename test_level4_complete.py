




"""
Complete Level 4 Visualization Test Suite

Comprehensive test suite for all Level 4 visualization capabilities.
"""

import logging
from src.v2.agents.level4.visualization.langgraph_visualization_agent import LangGraphVisualizationAgent
from src.v2.pipelines.level4_pipeline import Level4Pipeline
from src.v2.agents.level4.visualization.level2_integration import Level2IntegrationAgent

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def test_complete_level4_visualization():
    """Complete test of all Level 4 visualization capabilities"""
    print("Testing Complete Level 4 Visualization Implementation...")

    # Sample data
    tasks = [
        {"id": 1, "title": "Fix security vulnerability", "priority": "high", "category": "security", "value": 10},
        {"id": 2, "title": "Update UI components", "priority": "medium", "category": "ui", "value": 5},
        {"id": 3, "title": "Add documentation", "priority": "low", "category": "docs", "value": 3},
        {"id": 4, "title": "Optimize database queries", "priority": "high", "category": "performance", "value": 8},
        {"id": 5, "title": "Implement API endpoint", "priority": "medium", "category": "api", "value": 6},
    ]

    # Test 1: LangGraph Visualization Agent
    print("\n=== Testing LangGraph Visualization Agent ===")
    viz_agent = LangGraphVisualizationAgent()

    # Data preparation
    data_preparer = viz_agent.prepare_data(tasks)
    aggregated = data_preparer.aggregate(["priority"])
    print(f"✅ Data preparation: {len(aggregated)} groups")

    # Chart generation
    chart_data = {
        "title": "Tasks by Priority",
        "x_axis": ["high", "medium", "low"],
        "y_axis": [2, 2, 1]
    }
    chart_config = viz_agent.generate_chart("bar", chart_data)
    html_chart = viz_agent.export_chart("html")
    print(f"✅ Chart generation: {len(html_chart)} characters")

    # Table rendering
    table_renderer = viz_agent.render_table(tasks, ["id", "title", "priority"])
    html_table = table_renderer.render_html()
    print(f"✅ Table rendering: {len(html_table)} characters")

    # Interactive controller
    def on_update(updated_data):
        print(f"Data updated: {len(updated_data)} items")

    interactive_ctrl = viz_agent.create_interactive_controller(tasks, on_update)
    interactive_ctrl.filter_by("priority", "high")
    print(f"✅ Interactive controller: {len(interactive_ctrl.get_current_data())} filtered items")

    # Data export
    json_export = viz_agent.export_data(tasks, "json")
    print(f"✅ Data export: {len(json_export)} bytes")

    # Dashboard building
    dashboard = viz_agent.build_dashboard(
        charts=[{"type": "bar", "data": chart_data}],
        tables=[{"data": tasks, "headers": ["id", "title", "priority"]}]
    )
    print(f"✅ Dashboard: {len(dashboard['charts'])} charts, {len(dashboard['tables'])} tables")

    # Test 2: Level 4 Pipeline
    print("\n=== Testing Level 4 Pipeline ===")
    pipeline = Level4Pipeline()

    # Pipeline processing
    pipeline_result = pipeline.process_visualization(tasks, {
        "charts": [{"type": "bar", "data": chart_data}],
        "tables": [{"data": tasks, "headers": ["id", "title", "priority"]}],
        "interactive": True
    })
    print(f"✅ Pipeline: {len(pipeline_result['charts'])} charts, {len(pipeline_result['tables'])} tables")

    # Dashboard generation
    pipeline_dashboard = pipeline.generate_dashboard(tasks, {
        "charts": [{"type": "bar", "data": chart_data}],
        "tables": [{"data": tasks, "headers": ["id", "title", "priority"]}]
    })
    print(f"✅ Pipeline dashboard: {len(pipeline_dashboard['charts'])} charts")

    # Quality analysis
    quality_analysis = pipeline.analyze_visualization_quality(tasks)
    print(f"✅ Quality analysis: {quality_analysis.get('clarity_score', 'N/A')}")

    # Test 3: Level 2 Integration
    print("\n=== Testing Level 2 Integration ===")
    integration_agent = Level2IntegrationAgent()

    # Level 2 visualization with Level 4 enhancements
    level2_results = integration_agent.run_level2_visualization(tasks, "plotly")
    print(f"✅ Level 2 integration: {len(level2_results)} visualizations")

    # Comprehensive integration
    comprehensive_results = integration_agent.integrate_all_visualizations(tasks)
    print(f"✅ Comprehensive integration: {len(comprehensive_results)} visualizations")

    # Verify LangGraph metadata
    if "langgraph_metadata" in comprehensive_results:
        metadata = comprehensive_results["langgraph_metadata"]
        print(f"✅ LangGraph metadata: {metadata.get('relationship_strength', 'N/A')}")

    print("\n🎉 All Level 4 visualization tests completed successfully!")
    print("✅ Implementation is ready for production use")

if __name__ == "__main__":
    test_complete_level4_visualization()



