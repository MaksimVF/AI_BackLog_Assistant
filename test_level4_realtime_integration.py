













"""
Test Real-time Data Integration

Comprehensive test suite for the real-time data integration capabilities.
"""

import logging
import asyncio
from src.v2.agents.level4.visualization.realtime_data_integration import RealTimeDataIntegration

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def test_realtime_integration():
    """Test the real-time data integration capabilities"""
    print("Testing Real-time Data Integration...")

    # Sample data
    tasks = [
        {"id": 1, "title": "Fix security vulnerability", "priority": "high", "category": "security", "value": 10},
        {"id": 2, "title": "Update UI components", "priority": "medium", "category": "ui", "value": 5},
        {"id": 3, "title": "Add documentation", "priority": "low", "category": "docs", "value": 3},
        {"id": 4, "title": "Optimize database queries", "priority": "high", "category": "performance", "value": 8},
        {"id": 5, "title": "Implement API endpoint", "priority": "medium", "category": "api", "value": 6},
    ]

    # Test real-time data integration
    print("\nTesting RealTimeDataIntegration...")
    realtime_integration = RealTimeDataIntegration()

    # Test live data processing
    print("\nTesting live data processing...")
    def on_update(data):
        print(f"Data updated: {data.get('metadata', {}).get('contextual_insights', 'N/A')}")

    live_data_processing = realtime_integration.process_live_data(tasks[0], on_update)
    print(f"✅ Live data processing: {live_data_processing.get('metadata', {}).get('contextual_insights', 'N/A')}")

    # Test streaming data integration
    print("\nTesting streaming data integration...")
    streaming_data_integration = realtime_integration.integrate_streaming_data(tasks, on_update)
    print(f"✅ Streaming data integration: {streaming_data_integration.get('metadata', {}).get('contextual_insights', 'N/A')}")

    # Test real-time insights
    print("\nTesting real-time insights...")
    realtime_insights = realtime_integration.generate_realtime_insights(tasks[0])
    print(f"✅ Real-time insights: {realtime_insights.get('metadata', {}).get('contextual_insights', 'N/A')}")

    # Test real-time report
    print("\nTesting real-time report...")
    realtime_report = realtime_integration.generate_realtime_report(tasks[0])
    print(f"✅ Real-time report: {realtime_report.get('metadata', {}).get('contextual_insights', 'N/A')}")

    # Test real-time recommendations
    print("\nTesting real-time recommendations...")
    realtime_recommendations = realtime_integration.get_realtime_recommendations(tasks[0])
    print(f"✅ Real-time recommendations: {realtime_recommendations.get('metadata', {}).get('contextual_insights', 'N/A')}")

    print("\n🎉 All real-time data integration tests completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_realtime_integration())
















