
"""
Test script for visualization improvements.
"""

import json
from datetime import datetime, timedelta

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from visualization.visualization_aggregator import VisualizationAggregator


def generate_test_tasks():
    """Generate sample task data for testing visualizations."""
    today = datetime.now()

    tasks = [
        {
            "id": "task1",
            "title": "Implement User Authentication",
            "status": "completed",
            "priority": "high",
            "value": 8.5,
            "effort": 5.0,
            "start_date": (today - timedelta(days=10)).strftime("%Y-%m-%d"),
            "end_date": (today - timedelta(days=5)).strftime("%Y-%m-%d"),
            "dependencies": [],
            "metadata": {"team": "backend", "risk": "low"}
        },
        {
            "id": "task2",
            "title": "Design Database Schema",
            "status": "in_progress",
            "priority": "medium",
            "value": 6.0,
            "effort": 3.0,
            "start_date": (today - timedelta(days=3)).strftime("%Y-%m-%d"),
            "end_date": (today + timedelta(days=2)).strftime("%Y-%m-%d"),
            "dependencies": ["task1"],
            "metadata": {"team": "backend", "risk": "medium"}
        },
        {
            "id": "task3",
            "title": "Create API Documentation",
            "status": "planned",
            "priority": "low",
            "value": 4.0,
            "effort": 2.0,
            "start_date": (today + timedelta(days=1)).strftime("%Y-%m-%d"),
            "end_date": (today + timedelta(days=4)).strftime("%Y-%m-%d"),
            "dependencies": ["task2"],
            "metadata": {"team": "docs", "risk": "low"}
        },
        {
            "id": "task4",
            "title": "Frontend Integration",
            "status": "planned",
            "priority": "high",
            "value": 9.0,
            "effort": 7.0,
            "start_date": (today + timedelta(days=5)).strftime("%Y-%m-%d"),
            "end_date": (today + timedelta(days=12)).strftime("%Y-%m-%d"),
            "dependencies": ["task1", "task2"],
            "metadata": {"team": "frontend", "risk": "high"}
        },
        {
            "id": "task5",
            "title": "Testing and QA",
            "status": "planned",
            "priority": "medium",
            "value": 7.0,
            "effort": 4.0,
            "start_date": (today + timedelta(days=10)).strftime("%Y-%m-%d"),
            "end_date": (today + timedelta(days=15)).strftime("%Y-%m-%d"),
            "dependencies": ["task3", "task4"],
            "metadata": {"team": "qa", "risk": "medium"}
        }
    ]

    return tasks

def test_visualizations():
    """Test all visualization improvements."""
    print("Testing visualization improvements...")

    # Generate test data
    tasks = generate_test_tasks()

    # Create visualizations
    viz = VisualizationAggregator()
    results = viz.run(tasks, output_format="plotly")

    # Test HTML output
    html_output = viz.to_html(results)

    # Save HTML output for inspection
    with open("visualization_test_output.html", "w") as f:
        f.write(html_output)

    print("✓ Visualization test completed successfully!")
    print(f"✓ Generated HTML output to visualization_test_output.html")
    print(f"✓ Created {len(results)} visualizations:")
    for key in results.keys():
        if not key.endswith("_error"):
            print(f"  - {key}")

    # Test static output
    static_results = viz.run(tasks, output_format="static")
    print(f"✓ Generated {len(static_results)} static images")

    return results, static_results

if __name__ == "__main__":
    test_visualizations()
