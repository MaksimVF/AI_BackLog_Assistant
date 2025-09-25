




"""
Test Level 4 and Level 2 Visualization Integration

Comprehensive test suite for the integration between Level 4 visualization agents
and existing Level 2 visualization capabilities.
"""

import logging
from src.v2.agents.level4.visualization.level2_integration import Level2IntegrationAgent

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def test_level2_level4_integration():
    """Test the integration between Level 2 and Level 4 visualization agents"""
    print("Testing Level 2 and Level 4 Visualization Integration...")

    # Create integration agent
    integration_agent = Level2IntegrationAgent()

    # Sample data
    tasks = [
        {"id": 1, "title": "Fix security vulnerability", "priority": "high", "category": "security", "value": 10},
        {"id": 2, "title": "Update UI components", "priority": "medium", "category": "ui", "value": 5},
        {"id": 3, "title": "Add documentation", "priority": "low", "category": "docs", "value": 3},
        {"id": 4, "title": "Optimize database queries", "priority": "high", "category": "performance", "value": 8},
        {"id": 5, "title": "Implement API endpoint", "priority": "medium", "category": "api", "value": 6},
    ]

    # Test Level 2 visualization with Level 4 enhancements
    print("\nTesting Level 2 visualization with Level 4 enhancements...")
    level2_results = integration_agent.run_level2_visualization(tasks, "plotly")
    print(f"Level 2 visualization results: {list(level2_results.keys())}")

    # Test dependency graph generation
    print("\nTesting dependency graph generation...")
    dependency_graph = integration_agent.generate_dependency_graph(tasks)
    print(f"Dependency graph generated: {list(dependency_graph.keys())}")

    # Test heatmap generation
    print("\nTesting heatmap generation...")
    heatmap = integration_agent.generate_heatmap(tasks)
    print(f"Heatmap generated: {list(heatmap.keys())}")

    # Test dashboard generation
    print("\nTesting dashboard generation...")
    dashboard = integration_agent.generate_dashboard(tasks)
    print(f"Dashboard generated: {list(dashboard.keys())}")

    # Test timeline generation
    print("\nTesting timeline generation...")
    timeline = integration_agent.generate_timeline(tasks)
    print(f"Timeline generated: {list(timeline.keys())}")

    # Test comprehensive integration
    print("\nTesting comprehensive integration...")
    comprehensive_results = integration_agent.integrate_all_visualizations(tasks)
    print(f"Comprehensive results: {list(comprehensive_results.keys())}")

    # Verify LangGraph metadata
    if "langgraph_metadata" in comprehensive_results:
        metadata = comprehensive_results["langgraph_metadata"]
        print(f"LangGraph metadata: {metadata}")
        print("✅ LangGraph metadata successfully integrated")

    print("All Level 2 and Level 4 integration tests completed successfully!")

if __name__ == "__main__":
    test_level2_level4_integration()


