








"""
Test Advanced Visualization Types

Comprehensive test suite for the advanced visualization capabilities.
"""

import logging
from src.v2.agents.level4.visualization.network_graph_generator import NetworkGraphGenerator

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def test_advanced_visualization():
    """Test the advanced visualization capabilities"""
    print("Testing Advanced Visualization Types...")

    # Sample data with relationships
    tasks = [
        {"id": 1, "title": "Fix security vulnerability", "priority": "high", "category": "security", "value": 10, "related_to": [2, 3]},
        {"id": 2, "title": "Update UI components", "priority": "medium", "category": "ui", "value": 5, "related_to": [1]},
        {"id": 3, "title": "Add documentation", "priority": "low", "category": "docs", "value": 3, "related_to": [1]},
        {"id": 4, "title": "Optimize database queries", "priority": "high", "category": "performance", "value": 8, "related_to": [5]},
        {"id": 5, "title": "Implement API endpoint", "priority": "medium", "category": "api", "value": 6, "related_to": [4]},
    ]

    # Test network graph generator
    print("\nTesting NetworkGraphGenerator...")
    graph_generator = NetworkGraphGenerator()

    # Test basic network graph
    print("\nTesting basic network graph...")
    basic_graph = graph_generator.generate_network_graph(tasks, "basic")
    print(f"✅ Basic graph: {basic_graph.get('metadata', {}).get('contextual_insights', 'N/A')}")

    # Test community network graph
    print("\nTesting community network graph...")
    community_graph = graph_generator.generate_network_graph(tasks, "community")
    print(f"✅ Community graph: {community_graph.get('metadata', {}).get('contextual_insights', 'N/A')}")

    # Test centrality network graph
    print("\nTesting centrality network graph...")
    centrality_graph = graph_generator.generate_network_graph(tasks, "centrality")
    print(f"✅ Centrality graph: {centrality_graph.get('metadata', {}).get('contextual_insights', 'N/A')}")

    # Test 3D network graph
    print("\nTesting 3D network graph...")
    graph_3d = graph_generator.generate_network_graph(tasks, "3d")
    print(f"✅ 3D graph: {graph_3d.get('metadata', {}).get('contextual_insights', 'N/A')}")

    # Test network analysis
    print("\nTesting network analysis...")
    network_analysis = graph_generator.generate_network_analysis(tasks)
    print(f"✅ Network analysis: {network_analysis.get('metadata', {}).get('contextual_insights', 'N/A')}")

    # Test network insights
    print("\nTesting network insights...")
    network_insights = graph_generator.generate_network_insights(tasks)
    print(f"✅ Network insights: {network_insights.get('metadata', {}).get('contextual_insights', 'N/A')}")

    print("\n🎉 All advanced visualization tests completed successfully!")

if __name__ == "__main__":
    test_advanced_visualization()









