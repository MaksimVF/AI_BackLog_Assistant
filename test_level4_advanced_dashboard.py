
















"""
Test Advanced Dashboard Capabilities

Comprehensive test suite for the advanced dashboard capabilities.
"""

import logging
from src.v2.agents.level4.visualization.advanced_dashboard_generator import AdvancedDashboardGenerator

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def test_advanced_dashboard():
    """Test the advanced dashboard capabilities"""
    print("Testing Advanced Dashboard Capabilities...")

    # Sample data
    tasks = [
        {"id": 1, "title": "Fix security vulnerability", "priority": "high", "category": "security", "value": 10},
        {"id": 2, "title": "Update UI components", "priority": "medium", "category": "ui", "value": 5},
        {"id": 3, "title": "Add documentation", "priority": "low", "category": "docs", "value": 3},
        {"id": 4, "title": "Optimize database queries", "priority": "high", "category": "performance", "value": 8},
        {"id": 5, "title": "Implement API endpoint", "priority": "medium", "category": "api", "value": 6},
    ]

    # Test advanced dashboard generator
    print("\nTesting AdvancedDashboardGenerator...")
    dashboard_generator = AdvancedDashboardGenerator()

    # Test grid dashboard
    print("\nTesting grid dashboard...")
    grid_dashboard = dashboard_generator.generate_dashboard(tasks, "grid", "Grid Dashboard")
    print(f"✅ Grid dashboard: {grid_dashboard.get('metadata', {}).get('contextual_insights', 'N/A')}")

    # Test flex dashboard
    print("\nTesting flex dashboard...")
    flex_dashboard = dashboard_generator.generate_dashboard(tasks, "flex", "Flex Dashboard")
    print(f"✅ Flex dashboard: {flex_dashboard.get('metadata', {}).get('contextual_insights', 'N/A')}")

    # Test tabbed dashboard
    print("\nTesting tabbed dashboard...")
    tabbed_dashboard = dashboard_generator.generate_dashboard(tasks, "tabbed", "Tabbed Dashboard")
    print(f"✅ Tabbed dashboard: {tabbed_dashboard.get('metadata', {}).get('contextual_insights', 'N/A')}")

    # Test drill-down dashboard
    print("\nTesting drill-down dashboard...")
    drilldown_dashboard = dashboard_generator.generate_drilldown_dashboard(tasks, "Drilldown Dashboard")
    print(f"✅ Drill-down dashboard: {drilldown_dashboard.get('metadata', {}).get('contextual_insights', 'N/A')}")

    # Test customizable dashboard
    print("\nTesting customizable dashboard...")
    customizable_dashboard = dashboard_generator.generate_customizable_dashboard(tasks, "grid", "Customizable Dashboard")
    print(f"✅ Customizable dashboard: {customizable_dashboard.get('metadata', {}).get('contextual_insights', 'N/A')}")

    # Test dashboard insights
    print("\nTesting dashboard insights...")
    dashboard_insights = dashboard_generator.generate_dashboard_insights(tasks)
    print(f"✅ Dashboard insights: {dashboard_insights.get('metadata', {}).get('contextual_insights', 'N/A')}")

    # Test dashboard report
    print("\nTesting dashboard report...")
    dashboard_report = dashboard_generator.generate_dashboard_report(tasks)
    print(f"✅ Dashboard report: {dashboard_report.get('metadata', {}).get('contextual_insights', 'N/A')}")

    # Test dashboard recommendations
    print("\nTesting dashboard recommendations...")
    dashboard_recommendations = dashboard_generator.get_dashboard_recommendations(tasks)
    print(f"✅ Dashboard recommendations: {dashboard_recommendations.get('metadata', {}).get('contextual_insights', 'N/A')}")

    print("\n🎉 All advanced dashboard capabilities tests completed successfully!")

if __name__ == "__main__":
    test_advanced_dashboard()




















