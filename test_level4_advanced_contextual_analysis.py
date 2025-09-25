





"""
Test Advanced Contextual Analysis

Comprehensive test suite for the advanced contextual analysis capabilities.
"""

import logging
from src.v2.agents.level4.visualization.advanced_contextual_analysis import AdvancedContextualAnalysis
from src.v2.agents.level4.visualization.langgraph_data_preparer import LangGraphDataPreparer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def test_advanced_contextual_analysis():
    """Test the advanced contextual analysis capabilities"""
    print("Testing Advanced Contextual Analysis...")

    # Sample data with relationships
    tasks = [
        {"id": 1, "title": "Fix security vulnerability", "priority": "high", "category": "security", "value": 10, "related_to": [2, 3]},
        {"id": 2, "title": "Update UI components", "priority": "medium", "category": "ui", "value": 5, "related_to": [1]},
        {"id": 3, "title": "Add documentation", "priority": "low", "category": "docs", "value": 3, "related_to": [1]},
        {"id": 4, "title": "Optimize database queries", "priority": "high", "category": "performance", "value": 8, "related_to": [5]},
        {"id": 5, "title": "Implement API endpoint", "priority": "medium", "category": "api", "value": 6, "related_to": [4]},
    ]

    # Test advanced contextual analysis
    print("\nTesting AdvancedContextualAnalysis...")
    analysis = AdvancedContextualAnalysis()
    analysis_results = analysis.analyze_relationships(tasks)

    print(f"✅ Analysis results: {list(analysis_results.keys())}")
    print(f"✅ Communities detected: {analysis_results.get('communities', {}).get('num_communities', 0)}")
    print(f"✅ Centrality measures: {list(analysis_results.get('centrality', {}).keys())}")
    print(f"✅ Anomalies detected: {analysis_results.get('anomalies', {}).get('anomaly_count', 0)}")

    # Test insights generation
    insights = analysis.get_insights(tasks)
    print(f"✅ Insights: {list(insights.keys())}")
    print(f"✅ Recommendations: {insights.get('recommendations', [])}")

    # Test enhanced data preparer
    print("\nTesting Enhanced LangGraphDataPreparer...")
    data_preparer = LangGraphDataPreparer(tasks)

    # Test validation
    is_valid = data_preparer.validate()
    print(f"✅ Validation: {'successful' if is_valid else 'failed'}")

    # Test cleaning
    data_preparer.clean()
    print("✅ Data cleaning completed")

    # Test aggregation
    aggregated = data_preparer.aggregate(["priority"])
    print(f"✅ Aggregation: {len(aggregated)} groups created")

    # Test prepared data
    prepared_data = data_preparer.get_prepared_data()
    print(f"✅ Prepared data: {len(prepared_data)} groups with advanced metadata")

    # Test insights
    data_insights = data_preparer.get_insights()
    print(f"✅ Data insights: {list(data_insights.keys())}")

    print("\n🎉 All advanced contextual analysis tests completed successfully!")

if __name__ == "__main__":
    test_advanced_contextual_analysis()






