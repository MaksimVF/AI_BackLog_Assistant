




"""
Test Visualization Agent
"""

from agents.visualization.visualization_agent import VisualizationAgent

def test_visualization_agent():
    """Test the visualization agent with sample data"""

    # Create visualization agent
    viz_agent = VisualizationAgent()

    # Sample data
    tasks = [
        {"id": 1, "title": "Fix security vulnerability", "priority": "high", "category": "security", "value": 10},
        {"id": 2, "title": "Update UI components", "priority": "medium", "category": "ui", "value": 5},
        {"id": 3, "title": "Add documentation", "priority": "low", "category": "docs", "value": 3},
        {"id": 4, "title": "Optimize database queries", "priority": "high", "category": "performance", "value": 8},
        {"id": 5, "title": "Implement API endpoint", "priority": "medium", "category": "api", "value": 6},
    ]

    # Test data preparation
    print("Testing Data Preparation...")
    data_preparer = viz_agent.prepare_data(tasks)
    aggregated = data_preparer.aggregate(["priority"])
    print(f"Aggregated data: {aggregated}")

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

if __name__ == "__main__":
    test_visualization_agent()




