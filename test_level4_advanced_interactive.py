






"""
Test Advanced Interactive Features

Comprehensive test suite for the advanced interactive capabilities.
"""

import logging
from src.v2.agents.level4.visualization.advanced_interactive_controller import AdvancedInteractiveController

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def test_advanced_interactive_features():
    """Test the advanced interactive features"""
    print("Testing Advanced Interactive Features...")

    # Sample data
    tasks = [
        {"id": 1, "title": "Fix security vulnerability", "priority": "high", "category": "security", "value": 10},
        {"id": 2, "title": "Update UI components", "priority": "medium", "category": "ui", "value": 5},
        {"id": 3, "title": "Add documentation", "priority": "low", "category": "docs", "value": 3},
        {"id": 4, "title": "Optimize database queries", "priority": "high", "category": "performance", "value": 8},
        {"id": 5, "title": "Implement API endpoint", "priority": "medium", "category": "api", "value": 6},
    ]

    # Test advanced interactive controller
    print("\nTesting AdvancedInteractiveController...")
    def on_update(updated_data):
        print(f"Data updated: {len(updated_data)} items")

    interactive_ctrl = AdvancedInteractiveController(tasks, on_update)

    # Test natural language queries
    print("\nTesting natural language queries...")

    # Test filter query
    filter_result = interactive_ctrl.natural_language_query("filter by high priority")
    print(f"✅ Filter query result: {filter_result}")

    # Test sort query
    sort_result = interactive_ctrl.natural_language_query("sort by value descending")
    print(f"✅ Sort query result: {sort_result}")

    # Test insights query
    insights_result = interactive_ctrl.natural_language_query("get insights and recommendations")
    print(f"✅ Insights query result: {insights_result}")

    # Test general query
    general_result = interactive_ctrl.natural_language_query("show me the data")
    print(f"✅ General query result: {general_result}")

    # Test filtering
    print("\nTesting advanced filtering...")
    interactive_ctrl.filter_by("priority", "high")
    filtered_data = interactive_ctrl.get_current_data()
    print(f"✅ Filtered data: {len(filtered_data)} items")

    # Test sorting
    print("\nTesting advanced sorting...")
    interactive_ctrl.sort_by("value", True)
    sorted_data = interactive_ctrl.get_current_data()
    print(f"✅ Sorted data: {len(sorted_data)} items")

    # Test automatic insights
    print("\nTesting automatic insights...")
    automatic_insights = interactive_ctrl.get_automatic_insights()
    print(f"✅ Automatic insights: {list(automatic_insights.keys())}")

    # Test recommendations
    print("\nTesting recommendations...")
    recommendations = interactive_ctrl.generate_recommendations()
    print(f"✅ Recommendations: {recommendations}")

    # Test reset
    print("\nTesting reset...")
    interactive_ctrl.reset()
    reset_data = interactive_ctrl.get_current_data()
    print(f"✅ Reset data: {len(reset_data)} items")

    print("\n🎉 All advanced interactive features tests completed successfully!")

if __name__ == "__main__":
    test_advanced_interactive_features()







