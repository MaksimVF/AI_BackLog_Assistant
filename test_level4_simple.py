




"""
Simple Level 4 Visualization Test

Basic test to verify the Level 4 visualization implementation.
"""

import logging
from src.v2.agents.level4.visualization.langgraph_visualization_agent import LangGraphVisualizationAgent

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def test_simple_level4():
    """Simple test of Level 4 visualization"""
    print("Testing Level 4 Visualization...")

    # Create visualization agent
    viz_agent = LangGraphVisualizationAgent()

    # Sample data
    tasks = [
        {"id": 1, "title": "Fix security vulnerability", "priority": "high", "category": "security"},
        {"id": 2, "title": "Update UI components", "priority": "medium", "category": "ui"},
        {"id": 3, "title": "Add documentation", "priority": "low", "category": "docs"},
    ]

    # Test data preparation
    print("Testing data preparation...")
    data_preparer = viz_agent.prepare_data(tasks)
    aggregated = data_preparer.aggregate(["priority"])
    print(f"✅ Data preparation: {len(aggregated)} groups")

    # Test chart generation
    print("Testing chart generation...")
    chart_data = {
        "title": "Tasks by Priority",
        "x_axis": ["high", "medium", "low"],
        "y_axis": [1, 1, 1]
    }
    chart_config = viz_agent.generate_chart("bar", chart_data)
    print("✅ Chart generation: success")

    # Test table rendering
    print("Testing table rendering...")
    table_renderer = viz_agent.render_table(tasks, ["id", "title", "priority"])
    html_table = table_renderer.render_html()
    print(f"✅ Table rendering: {len(html_table)} characters")

    print("✅ Level 4 visualization test completed successfully!")

if __name__ == "__main__":
    test_simple_level4()




