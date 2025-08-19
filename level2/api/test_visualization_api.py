

"""
Test script for visualization improvements.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from visualization.visualization_aggregator import VisualizationAggregator

def test_visualization_direct():
    """Test the visualization aggregator directly."""
    print("Testing visualization aggregator...")

    # Test data
    test_tasks = [
        {
            "id": "task1",
            "title": "Implement User Authentication",
            "status": "completed",
            "priority": "high",
            "value": 8.5,
            "effort": 5.0,
            "start_date": "2025-08-01",
            "end_date": "2025-08-05",
            "dependencies": []
        },
        {
            "id": "task2",
            "title": "Design Database Schema",
            "status": "in_progress",
            "priority": "medium",
            "value": 6.0,
            "effort": 3.0,
            "start_date": "2025-08-03",
            "end_date": "2025-08-07",
            "dependencies": ["task1"]
        },
        {
            "id": "task3",
            "title": "Create API Documentation",
            "status": "planned",
            "priority": "low",
            "value": 4.0,
            "effort": 2.0,
            "start_date": "2025-08-06",
            "end_date": "2025-08-09",
            "dependencies": ["task2"]
        }
    ]

    try:
        # Test interactive visualizations
        viz = VisualizationAggregator()
        results = viz.run(test_tasks, output_format="plotly")

        print(f"✓ Successfully generated {len(results)} interactive visualizations:")
        for key in results.keys():
            if not key.endswith("_error"):
                print(f"  - {key}")

        # Test HTML generation
        html_content = viz.to_html(results)
        print(f"✓ Generated HTML content (length: {len(html_content)} chars)")

        # Test static visualizations
        static_results = viz.run(test_tasks, output_format="static")
        print(f"✓ Successfully generated {len(static_results)} static images")

        print("✓ Visualization aggregator test completed successfully!")

    except Exception as e:
        print(f"✗ Error in visualization test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_visualization_direct()

