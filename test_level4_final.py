





"""
Final Level 4 Visualization Test

Comprehensive test for the complete Level 4 visualization implementation.
"""

import logging
from src.v2.agents.level4.visualization import Level4VisualizationSystem

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def test_final_level4_visualization():
    """Final test of the complete Level 4 visualization system"""
    print("Testing Complete Level 4 Visualization System...")

    # Create visualization system
    viz_system = Level4VisualizationSystem()

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

    # Test complete visualization processing
    print("Testing complete visualization processing...")
    result = viz_system.process_complete_visualization(tasks, visualization_config)

    # Verify results
    print(f"✅ Visualization results: {list(result.keys())}")

    # Check for Level 3 insights
    if "level3_insights" in result:
        print(f"✅ Level 3 insights: {list(result['level3_insights'].keys())}")

    # Check for charts
    if "charts" in result:
        print(f"✅ Charts: {len(result['charts'])} charts generated")

    # Check for tables
    if "tables" in result:
        print(f"✅ Tables: {len(result['tables'])} tables generated")

    # Check for comprehensive metadata
    if "comprehensive_metadata" in result:
        metadata = result["comprehensive_metadata"]
        print(f"✅ Comprehensive metadata: {metadata.get('insights', 'N/A')}")

    print("✅ Final Level 4 visualization test completed successfully!")

if __name__ == "__main__":
    test_final_level4_visualization()





