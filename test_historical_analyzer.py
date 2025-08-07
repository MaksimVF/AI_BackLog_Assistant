





import sys
import os
import json
import time
from datetime import datetime, timedelta

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.system_admin.historical_analyzer import HistoricalAnalyzer

def generate_test_data():
    """Generate test data for historical analysis"""
    test_data = {
        'cpu_usage': [],
        'memory_usage': [],
        'disk_usage': [],
        'process_count': [],
        'response_times': [],
        'error_rates': [],
        'timestamps': []
    }

    # Generate data for the past 30 days
    base_date = datetime.now() - timedelta(days=30)

    for day in range(30):
        for hour in range(24):
            timestamp = (base_date + timedelta(days=day, hours=hour)).isoformat()

            # Generate values with patterns
            cpu = 30 + 10 * (day / 30) + 5 * (hour / 24)  # Increasing trend
            memory = 40 + 5 * (day / 30)  # Slow increase
            disk = 50 + 2 * day  # Steady increase
            processes = 100 + 10 * (hour / 24)  # Daily variation
            response_time = 50 + 20 * (hour / 24)  # Daily variation
            error_rate = 1 + 0.5 * (day / 30)  # Slow increase

            # Add some anomalies
            if day == 25 and hour == 12:  # Spike on day 25
                cpu += 40
                memory += 30
                error_rate += 10

            test_data['cpu_usage'].append({'timestamp': timestamp, 'value': cpu})
            test_data['memory_usage'].append({'timestamp': timestamp, 'value': memory})
            test_data['disk_usage'].append({'timestamp': timestamp, 'value': disk})
            test_data['process_count'].append({'timestamp': timestamp, 'value': processes})
            test_data['response_times'].append({'timestamp': timestamp, 'value': response_time})
            test_data['error_rates'].append({'timestamp': timestamp, 'value': error_rate})
            test_data['timestamps'].append(timestamp)

    return test_data

def test_historical_analyzer():
    """Test the historical analyzer"""
    print("=== Testing Historical Analyzer ===")

    # Test 1: Initialize analyzer
    print("\n1. Testing initialization...")
    analyzer = HistoricalAnalyzer()
    print("✓ HistoricalAnalyzer initialized")

    # Test 2: Generate and save test data
    print("\n2. Testing data collection...")
    test_data = generate_test_data()

    # Save test data to file
    os.makedirs('data', exist_ok=True)
    with open('data/historical_data.json', 'w') as f:
        json.dump(test_data, f)

    # Load the data
    analyzer.collect_historical_data()
    print("✓ Test data collected and loaded")

    # Test 3: Train models
    print("\n3. Testing model training...")
    analyzer.train_models()
    print("✓ Models trained successfully")

    # Test 4: Trend analysis
    print("\n4. Testing trend analysis...")
    cpu_trend = analyzer.analyze_trends('cpu_usage')
    print(f"CPU trend: {cpu_trend.get('trend', {}).get('direction', 'unknown')}")
    print(f"CPU anomalies: {len(cpu_trend.get('anomalies', []))}")
    print("✓ Trend analysis completed")

    # Test 5: Forecasting
    print("\n5. Testing forecasting...")
    cpu_forecast = analyzer.forecast_future_values('cpu_usage', horizon_days=7)
    print(f"CPU forecast: {len(cpu_forecast.get('forecast', []))} days")
    if cpu_forecast.get('forecast'):
        print(f"Last forecast value: {cpu_forecast['forecast'][-1]['predicted']:.2f}")
    print("✓ Forecasting completed")

    # Test 6: Issue prediction
    print("\n6. Testing issue prediction...")
    predictions = analyzer.predict_system_issues()
    print(f"Overall risk: {predictions.get('overall_risk', {}).get('overall_risk', 'unknown')}")
    print("Predicted issues:")
    for metric, pred in predictions.get('predictions', {}).items():
        issues = pred.get('issue_prediction', {}).get('predicted_issues', [])
        if issues:
            print(f"  {metric}: {', '.join(issues)}")
    print("✓ Issue prediction completed")

    # Test 7: Report generation
    print("\n7. Testing report generation...")
    report = analyzer.generate_report(days=30)
    print(f"Report contains {len(report.get('trend_analysis', {}))} trend analyses")
    print(f"Report risk: {report.get('issue_predictions', {}).get('overall_risk', {}).get('overall_risk', 'unknown')}")
    print("✓ Report generation completed")

    # Test 8: Logging integration
    print("\n8. Testing logging integration...")
    analyzer.log_historical_analysis(predictions)
    print("✓ Logging integration works")

    print("\n=== Historical Analyzer Test Complete ===")

if __name__ == "__main__":
    test_historical_analyzer()





