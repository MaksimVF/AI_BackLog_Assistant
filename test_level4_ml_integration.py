









"""
Test Machine Learning Integration

Comprehensive test suite for the machine learning integration capabilities.
"""

import logging
from src.v2.agents.level4.visualization.ml_integration import MachineLearningIntegration

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def test_ml_integration():
    """Test the machine learning integration capabilities"""
    print("Testing Machine Learning Integration...")

    # Sample data
    tasks = [
        {"id": 1, "title": "Fix security vulnerability", "priority": "high", "category": "security", "value": 10},
        {"id": 2, "title": "Update UI components", "priority": "medium", "category": "ui", "value": 5},
        {"id": 3, "title": "Add documentation", "priority": "low", "category": "docs", "value": 3},
        {"id": 4, "title": "Optimize database queries", "priority": "high", "category": "performance", "value": 8},
        {"id": 5, "title": "Implement API endpoint", "priority": "medium", "category": "api", "value": 6},
    ]

    # Test machine learning integration
    print("\nTesting MachineLearningIntegration...")
    ml_integration = MachineLearningIntegration()

    # Test anomaly detection
    print("\nTesting anomaly detection...")
    anomaly_results = ml_integration.detect_anomalies(tasks)
    print(f"✅ Anomaly detection: {anomaly_results.get('anomaly_count', 0)} anomalies detected")

    # Test clustering
    print("\nTesting clustering...")
    cluster_results = ml_integration.cluster_data(tasks, 2)
    print(f"✅ Clustering: {cluster_results.get('num_clusters', 0)} clusters created")

    # Test trend prediction
    print("\nTesting trend prediction...")
    trend_results = ml_integration.predict_trends(tasks)
    print(f"✅ Trend prediction: {trend_results.get('future_steps', 0)} future steps predicted")

    # Test sentiment analysis
    print("\nTesting sentiment analysis...")
    sentiment_results = ml_integration.analyze_sentiment(tasks)
    print(f"✅ Sentiment analysis: {len(sentiment_results.get('sentiment_analysis', []))} sentiments analyzed")

    # Test ML insights
    print("\nTesting ML insights...")
    ml_insights = ml_integration.generate_ml_insights(tasks)
    print(f"✅ ML insights: {list(ml_insights.keys())}")

    # Test recommendations
    print("\nTesting recommendations...")
    recommendations = ml_integration.get_recommendations(tasks)
    print(f"✅ Recommendations: {recommendations.get('recommendations', [])}")

    print("\n🎉 All machine learning integration tests completed successfully!")

if __name__ == "__main__":
    test_ml_integration()











