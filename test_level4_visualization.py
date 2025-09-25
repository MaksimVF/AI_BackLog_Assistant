



"""
Test Level 4 Visualization Agents

Comprehensive test suite for the new LangGraph-based visualization agents.
"""

import logging
from src.v2.agents.level4.visualization.langgraph_visualization_agent import LangGraphVisualizationAgent
from src.v2.pipelines.level4_pipeline import Level4Pipeline

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def test_langgraph_visualization_agent():
    """Test the LangGraph visualization agent with sample data"""
    print("Testing LangGraph Visualization Agent...")

    # Create visualization agent
    viz_agent = LangGraphVisualizationAgent()

    # Sample data
    tasks = [
        {"id": 1, "title": "Fix security vulnerability", "priority": "high", "category": "security", "value": 10},
        {"id": 2, "title": "Update UI components", "priority": "medium", "category": "ui", "value": 5},
        {"id": 3, "title": "Add documentation", "priority": "low", "category": "docs", "value": 3},
        {"id": 4, "title": "Optimize database queries", "priority": "high", "category": "performance", "value": 8},
        {"id": 5, "title": "Implement API endpoint", "priority": "medium", "category": "api", "value": 6},
    ]

    # Test data preparation
    print("\nTesting Data Preparation...")
    data_preparer = viz_agent.prepare_data(tasks)
    aggregated = data_preparer.aggregate(["priority"])
    print(f"Aggregated data: {len(aggregated)} groups")

    # Test chart generation
    print("\nTesting Chart Generation...")
    chart_data = {
        "title": "Tasks by Priority",
        "x_axis": ["high", "medium", "low"],
        "y_axis": [2, 2, 1]
    }
    chart_options = {
        "color_scheme": "pastel",
        "legend_position": "bottom",
        "title_font_size": 18
    }
    chart_config = viz_agent.generate_chart("bar", chart_data, chart_options)
    print("Chart configuration generated successfully")

    # Test chart export
    print("\nTesting Chart Export...")
    html_export = viz_agent.export_chart("html")
    print("HTML export generated (first 200 chars):")
    print(html_export[:200])

    # Test table rendering
    print("\nTesting Table Rendering...")
    table_renderer = viz_agent.render_table(tasks, ["id", "title", "priority", "category"])
    html_table = table_renderer.render_html()
    print("Table HTML generated (first 200 chars):")
    print(html_table[:200])

    # Test table export
    print("\nTesting Table Export...")
    csv_export = table_renderer.export_csv()
    print("CSV export generated (first 100 chars):")
    print(csv_export[:100])

    # Test interactive controller
    print("\nTesting Interactive Controller...")
    def on_update(updated_data):
        print(f"Data updated, now has {len(updated_data)} items")

    interactive_ctrl = viz_agent.create_interactive_controller(tasks, on_update)
    print("Filtering by priority='high'...")
    interactive_ctrl.filter_by("priority", "high")
    print(f"Filtered data: {len(interactive_ctrl.get_current_data())} items")

    # Test data export
    print("\nTesting Data Export...")
    json_export = viz_agent.export_data(tasks, "json")
    print("JSON export generated (first 100 chars):")
    print(json_export[:100].decode('utf-8'))

    # Test dashboard building
    print("\nTesting Dashboard Building...")
    dashboard = viz_agent.build_dashboard(
        charts=[{
            "type": "bar",
            "data": chart_data,
            "options": chart_options
        }],
        tables=[{
            "data": tasks,
            "headers": ["id", "title", "priority"]
        }]
    )
    print("Dashboard built successfully")
    print(f"Dashboard contains {len(dashboard['charts'])} charts and {len(dashboard['tables'])} tables")

    # Test visualization insights
    print("\nTesting Visualization Insights...")
    insights = viz_agent.get_visualization_insights()
    print(f"Visualization insights: {insights}")

    print("All tests completed successfully!")

def test_level4_pipeline():
    """Test the Level 4 pipeline"""
    print("\n\nTesting Level 4 Pipeline...")

    # Create pipeline
    pipeline = Level4Pipeline()

    # Sample data
    tasks = [
        {"id": 1, "title": "Fix security vulnerability", "priority": "high", "category": "security", "value": 10},
        {"id": 2, "title": "Update UI components", "priority": "medium", "category": "ui", "value": 5},
        {"id": 3, "title": "Add documentation", "priority": "low", "category": "docs", "value": 3},
        {"id": 4, "title": "Optimize database queries", "priority": "high", "category": "performance", "value": 8},
        {"id": 5, "title": "Implement API endpoint", "priority": "medium", "category": "api", "value": 6},
    ]

    # Visualization configuration
    visualization_config = {
        "charts": [
            {
                "type": "bar",
                "data": {
                    "title": "Tasks by Priority",
                    "x_axis": ["high", "medium", "low"],
                    "y_axis": [2, 2, 1]
                },
                "options": {
                    "color_scheme": "pastel",
                    "legend_position": "bottom"
                }
            }
        ],
        "tables": [
            {
                "data": tasks,
                "headers": ["id", "title", "priority", "category"]
            }
        ],
        "interactive": True
    }

    # Test pipeline processing
    result = pipeline.process_visualization(tasks, visualization_config)
    print("Level 4 pipeline processing completed")
    print(f"Result contains {len(result['charts'])} charts and {len(result['tables'])} tables")

    # Test dashboard generation
    dashboard = pipeline.generate_dashboard(tasks, visualization_config)
    print("Dashboard generation completed")
    print(f"Dashboard contains {len(dashboard['charts'])} charts and {len(dashboard['tables'])} tables")

    # Test quality analysis
    quality_analysis = pipeline.analyze_visualization_quality(tasks)
    print("Quality analysis completed")
    print(f"Quality score: {quality_analysis.get('clarity_score', 'N/A')}")

    print("Level 4 pipeline tests completed successfully!")

if __name__ == "__main__":
    test_langgraph_visualization_agent()
    test_level4_pipeline()

