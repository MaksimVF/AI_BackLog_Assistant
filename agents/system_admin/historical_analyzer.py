




import os
import sys
import time
import logging
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from prophet import Prophet  # Facebook's Prophet for time series forecasting

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base import BaseAgent
from .logging_manager import initialize_logging
from .monitoring_agent import MonitoringAgent

class HistoricalAnalyzer(BaseAgent):
    """
    HistoricalAnalyzer - Analyzes long-term trends and predicts system issues
    using historical data from monitoring and logging systems.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(name="HistoricalAnalyzer")
        self.config = config or {}
        self.logger = logging.getLogger("HistoricalAnalyzer")
        self.monitor = MonitoringAgent()

        # Initialize logging
        self.logging_manager = initialize_logging(
            service_name="HistoricalAnalyzer",
            environment=os.getenv('ENV', 'dev')
        )

        # Configuration parameters
        self.analysis_window_days = self.config.get('analysis_window_days', 30)
        self.forecast_horizon_days = self.config.get('forecast_horizon_days', 7)
        self.anomaly_contamination = self.config.get('anomaly_contamination', 0.05)
        self.data_storage_path = self.config.get('data_storage_path', 'data/historical_data.json')

        # Load historical data
        self.historical_data = self._load_historical_data()

        # Initialize models
        self.anomaly_detector = None
        self.forecast_models = {}
        self._initialize_models()

        self.logger.info("HistoricalAnalyzer initialized for long-term trend analysis")

    def _load_historical_data(self) -> Dict[str, Any]:
        """Load historical monitoring data from storage"""
        try:
            if os.path.exists(self.data_storage_path):
                with open(self.data_storage_path, 'r') as f:
                    return json.load(f)
            return {
                'cpu_usage': [],
                'memory_usage': [],
                'disk_usage': [],
                'process_count': [],
                'response_times': [],
                'error_rates': [],
                'timestamps': []
            }
        except Exception as e:
            self.logger.error(f"Failed to load historical data: {e}")
            return {
                'cpu_usage': [],
                'memory_usage': [],
                'disk_usage': [],
                'process_count': [],
                'response_times': [],
                'error_rates': [],
                'timestamps': []
            }

    def _save_historical_data(self):
        """Save historical data to storage"""
        try:
            os.makedirs(os.path.dirname(self.data_storage_path), exist_ok=True)
            with open(self.data_storage_path, 'w') as f:
                json.dump(self.historical_data, f)
        except Exception as e:
            self.logger.error(f"Failed to save historical data: {e}")

    def _initialize_models(self):
        """Initialize predictive models"""
        try:
            # Initialize anomaly detection model
            self.anomaly_detector = IsolationForest(
                contamination=self.anomaly_contamination,
                random_state=42
            )

            # Initialize forecast models for different metrics
            self.forecast_models = {
                'cpu_usage': self._create_forecast_model(),
                'memory_usage': self._create_forecast_model(),
                'disk_usage': self._create_forecast_model(),
                'process_count': self._create_forecast_model(),
                'response_times': self._create_forecast_model(),
                'error_rates': self._create_forecast_model()
            }

            self.logger.info("Predictive models initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize models: {e}")

    def _create_forecast_model(self):
        """Create a time series forecast model"""
        # Return a Prophet model for time series forecasting
        return Prophet(
            interval_width=0.95,
            yearly_seasonality=False,
            weekly_seasonality=True,
            daily_seasonality=True
        )

    def collect_historical_data(self, days: int = None) -> Dict[str, Any]:
        """Collect historical data from monitoring system"""
        try:
            days = days or self.analysis_window_days
            end_time = datetime.now()
            start_time = end_time - timedelta(days=days)

            # Get historical data from monitoring agent
            historical_metrics = self.monitor.get_historical_metrics(
                start_time=start_time,
                end_time=end_time
            )

            # Update our historical data
            for metric, values in historical_metrics.items():
                if metric in self.historical_data:
                    # Avoid duplicates
                    existing_timestamps = set(self.historical_data['timestamps'])
                    new_data = []
                    for entry in values:
                        if entry['timestamp'] not in existing_timestamps:
                            new_data.append(entry)
                            existing_timestamps.add(entry['timestamp'])

                    # Update the data
                    if metric != 'timestamps':
                        self.historical_data[metric].extend(new_data)
                    else:
                        # Timestamps are handled separately
                        pass

            # Sort data by timestamp
            for metric in self.historical_data:
                if metric != 'timestamps':
                    self.historical_data[metric].sort(key=lambda x: x['timestamp'])

            # Save updated data
            self._save_historical_data()

            return self.historical_data

        except Exception as e:
            self.logger.error(f"Failed to collect historical data: {e}")
            return self.historical_data

    def analyze_trends(self, metric: str, window_days: int = None) -> Dict[str, Any]:
        """Analyze long-term trends for a specific metric"""
        try:
            window_days = window_days or self.analysis_window_days

            # Get data for the specified window
            data = self._get_recent_data(metric, window_days)

            if not data or len(data) < 2:
                return {
                    'metric': metric,
                    'status': 'insufficient_data',
                    'message': 'Not enough data for trend analysis'
                }

            # Convert to DataFrame for analysis
            df = pd.DataFrame(data)

            # Calculate basic statistics
            trend_analysis = {
                'metric': metric,
                'count': len(df),
                'mean': df['value'].mean(),
                'median': df['value'].median(),
                'std': df['value'].std(),
                'min': df['value'].min(),
                'max': df['value'].max(),
                'trend': self._calculate_trend(df),
                'seasonality': self._detect_seasonality(df),
                'anomalies': self._detect_anomalies(df)
            }

            return trend_analysis

        except Exception as e:
            self.logger.error(f"Failed to analyze trends for {metric}: {e}")
            return {
                'metric': metric,
                'status': 'error',
                'message': str(e)
            }

    def _get_recent_data(self, metric: str, days: int) -> List[Dict[str, Any]]:
        """Get recent data for a specific metric"""
        try:
            if metric not in self.historical_data:
                return []

            end_time = datetime.now()
            start_time = end_time - timedelta(days=days)

            # Filter data by time window
            recent_data = [
                entry for entry in self.historical_data[metric]
                if start_time <= datetime.fromisoformat(entry['timestamp']) <= end_time
            ]

            return recent_data

        except Exception as e:
            self.logger.error(f"Failed to get recent data for {metric}: {e}")
            return []

    def _calculate_trend(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate trend using linear regression"""
        try:
            # Add time index
            df['time_index'] = range(len(df))

            # Fit linear regression
            slope, intercept = np.polyfit(df['time_index'], df['value'], 1)

            return {
                'slope': slope,
                'intercept': intercept,
                'direction': 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable',
                'strength': abs(slope)
            }

        except Exception as e:
            self.logger.error(f"Failed to calculate trend: {e}")
            return {
                'slope': 0,
                'intercept': 0,
                'direction': 'unknown',
                'strength': 0
            }

    def _detect_seasonality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect seasonality patterns"""
        try:
            # Check for daily patterns
            df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
            hourly_mean = df.groupby('hour')['value'].mean()

            # Check for weekly patterns
            df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
            daily_mean = df.groupby('day_of_week')['value'].mean()

            return {
                'has_daily_pattern': hourly_mean.std() > 0.1 * df['value'].std(),
                'has_weekly_pattern': daily_mean.std() > 0.1 * df['value'].std(),
                'hourly_pattern': hourly_mean.to_dict(),
                'daily_pattern': daily_mean.to_dict()
            }

        except Exception as e:
            self.logger.error(f"Failed to detect seasonality: {e}")
            return {
                'has_daily_pattern': False,
                'has_weekly_pattern': False,
                'hourly_pattern': {},
                'daily_pattern': {}
            }

    def _detect_anomalies(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect anomalies using Isolation Forest"""
        try:
            # Prepare data for anomaly detection
            X = df[['value']].values

            # Fit model if not already fitted
            if not hasattr(self.anomaly_detector, 'estimators_'):
                self.anomaly_detector.fit(X)

            # Predict anomalies
            df['anomaly_score'] = self.anomaly_detector.decision_function(X)
            df['is_anomaly'] = self.anomaly_detector.predict(X) == -1

            # Get anomalies
            anomalies = df[df['is_anomaly']][['timestamp', 'value', 'anomaly_score']].to_dict('records')

            return anomalies

        except Exception as e:
            self.logger.error(f"Failed to detect anomalies: {e}")
            return []

    def forecast_future_values(self, metric: str, horizon_days: int = None) -> Dict[str, Any]:
        """Forecast future values using time series analysis"""
        try:
            horizon_days = horizon_days or self.forecast_horizon_days

            # Get recent data
            data = self._get_recent_data(metric, self.analysis_window_days)

            if len(data) < 2:
                return {
                    'metric': metric,
                    'status': 'insufficient_data',
                    'message': 'Not enough data for forecasting'
                }

            # Prepare data for Prophet
            df = pd.DataFrame({
                'ds': pd.to_datetime([entry['timestamp'] for entry in data]),
                'y': [entry['value'] for entry in data]
            })

            # Fit model
            model = self.forecast_models.get(metric)
            if not model:
                model = self._create_forecast_model()
                self.forecast_models[metric] = model

            model.fit(df)

            # Make future dataframe
            future = model.make_future_dataframe(periods=horizon_days)

            # Make prediction
            forecast = model.predict(future)

            # Extract relevant information
            forecast_data = forecast.tail(horizon_days)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].rename(
                columns={'ds': 'timestamp', 'yhat': 'predicted', 'yhat_lower': 'lower', 'yhat_upper': 'upper'}
            )

            return {
                'metric': metric,
                'status': 'success',
                'forecast': forecast_data.to_dict('records'),
                'model_summary': model.params
            }

        except Exception as e:
            self.logger.error(f"Failed to forecast {metric}: {e}")
            return {
                'metric': metric,
                'status': 'error',
                'message': str(e)
            }

    def predict_system_issues(self) -> Dict[str, Any]:
        """Predict potential system issues based on historical trends"""
        try:
            predictions = {}

            # Analyze key metrics
            key_metrics = ['cpu_usage', 'memory_usage', 'disk_usage', 'error_rates']

            for metric in key_metrics:
                # Get trend analysis
                trend = self.analyze_trends(metric)

                # Get forecast
                forecast = self.forecast_future_values(metric)

                # Predict issues
                issue_prediction = self._predict_issue_from_trend(trend, forecast)

                predictions[metric] = {
                    'trend': trend,
                    'forecast': forecast,
                    'issue_prediction': issue_prediction
                }

            return {
                'status': 'success',
                'predictions': predictions,
                'overall_risk': self._calculate_overall_risk(predictions)
            }

        except Exception as e:
            self.logger.error(f"Failed to predict system issues: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }

    def _predict_issue_from_trend(self, trend: Dict[str, Any], forecast: Dict[str, Any]) -> Dict[str, Any]:
        """Predict specific issues from trend and forecast"""
        try:
            metric = trend.get('metric')

            # Check for anomalies
            has_anomalies = len(trend.get('anomalies', [])) > 0

            # Check trend direction
            trend_direction = trend.get('trend', {}).get('direction', 'stable')
            trend_strength = trend.get('trend', {}).get('strength', 0)

            # Check forecast
            forecast_values = forecast.get('forecast', [])
            if forecast_values:
                avg_forecast = np.mean([entry['predicted'] for entry in forecast_values])
                max_forecast = max([entry['predicted'] for entry in forecast_values])
            else:
                avg_forecast = 0
                max_forecast = 0

            # Predict issues based on thresholds
            issue_prediction = {
                'has_anomalies': has_anomalies,
                'trend_direction': trend_direction,
                'trend_strength': trend_strength,
                'avg_forecast': avg_forecast,
                'max_forecast': max_forecast,
                'risk_level': 'low',
                'predicted_issues': []
            }

            # CPU usage prediction
            if metric == 'cpu_usage':
                if max_forecast > 90:
                    issue_prediction['risk_level'] = 'high'
                    issue_prediction['predicted_issues'].append('CPU overload')
                elif avg_forecast > 80:
                    issue_prediction['risk_level'] = 'medium'
                    issue_prediction['predicted_issues'].append('High CPU usage')

            # Memory usage prediction
            elif metric == 'memory_usage':
                if max_forecast > 90:
                    issue_prediction['risk_level'] = 'high'
                    issue_prediction['predicted_issues'].append('Memory exhaustion')
                elif avg_forecast > 80:
                    issue_prediction['risk_level'] = 'medium'
                    issue_prediction['predicted_issues'].append('High memory usage')

            # Disk usage prediction
            elif metric == 'disk_usage':
                if max_forecast > 90:
                    issue_prediction['risk_level'] = 'high'
                    issue_prediction['predicted_issues'].append('Disk full')
                elif avg_forecast > 80:
                    issue_prediction['risk_level'] = 'medium'
                    issue_prediction['predicted_issues'].append('High disk usage')

            # Error rate prediction
            elif metric == 'error_rates':
                if max_forecast > 10:  # More than 10% error rate
                    issue_prediction['risk_level'] = 'high'
                    issue_prediction['predicted_issues'].append('High error rate')
                elif avg_forecast > 5:  # More than 5% error rate
                    issue_prediction['risk_level'] = 'medium'
                    issue_prediction['predicted_issues'].append('Increased errors')

            return issue_prediction

        except Exception as e:
            self.logger.error(f"Failed to predict issue from trend: {e}")
            return {
                'risk_level': 'unknown',
                'predicted_issues': [],
                'message': str(e)
            }

    def _calculate_overall_risk(self, predictions: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall system risk based on individual predictions"""
        try:
            risk_scores = []

            for metric, prediction in predictions.items():
                issue_pred = prediction.get('issue_prediction', {})
                risk_level = issue_pred.get('risk_level', 'low')

                # Convert risk level to score
                if risk_level == 'high':
                    risk_scores.append(3)
                elif risk_level == 'medium':
                    risk_scores.append(2)
                else:
                    risk_scores.append(1)

            # Calculate overall risk
            avg_risk = np.mean(risk_scores) if risk_scores else 1

            if avg_risk >= 2.5:
                overall_risk = 'high'
            elif avg_risk >= 1.5:
                overall_risk = 'medium'
            else:
                overall_risk = 'low'

            return {
                'overall_risk': overall_risk,
                'risk_score': avg_risk,
                'recommendations': self._generate_recommendations(overall_risk, predictions)
            }

        except Exception as e:
            self.logger.error(f"Failed to calculate overall risk: {e}")
            return {
                'overall_risk': 'unknown',
                'risk_score': 0,
                'recommendations': []
            }

    def _generate_recommendations(self, risk_level: str, predictions: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on risk level"""
        recommendations = []

        if risk_level == 'high':
            recommendations.append("Immediately review system resources and performance")
            recommendations.append("Consider scaling up resources or optimizing workloads")

            # Specific recommendations based on metrics
            for metric, prediction in predictions.items():
                issues = prediction.get('issue_prediction', {}).get('predicted_issues', [])
                if issues:
                    if 'CPU overload' in issues:
                        recommendations.append("Optimize CPU-intensive processes")
                    if 'Memory exhaustion' in issues:
                        recommendations.append("Increase memory allocation or optimize memory usage")
                    if 'Disk full' in issues:
                        recommendations.append("Clean up disk space or add storage")
                    if 'High error rate' in issues:
                        recommendations.append("Investigate and fix error sources")

        elif risk_level == 'medium':
            recommendations.append("Monitor system closely for potential issues")
            recommendations.append("Review resource usage trends")

        else:
            recommendations.append("System appears stable, continue normal monitoring")

        return recommendations

    def train_models(self, force_retrain: bool = False):
        """Train predictive models with current data"""
        try:
            if not force_retrain and self.anomaly_detector and hasattr(self.anomaly_detector, 'estimators_'):
                self.logger.info("Models already trained, use force_retrain=True to retrain")
                return True

            # Collect fresh data
            self.collect_historical_data()

            # Prepare data for training
            all_data = []
            for metric in ['cpu_usage', 'memory_usage', 'disk_usage', 'error_rates']:
                data = self._get_recent_data(metric, self.analysis_window_days)
                if data:
                    all_data.extend([entry['value'] for entry in data])

            if len(all_data) < 10:
                self.logger.warning("Not enough data for model training")
                return False

            # Train anomaly detector
            X = np.array(all_data).reshape(-1, 1)
            self.anomaly_detector.fit(X)

            # Train forecast models
            for metric in ['cpu_usage', 'memory_usage', 'disk_usage', 'error_rates']:
                data = self._get_recent_data(metric, self.analysis_window_days)
                if len(data) >= 2:
                    df = pd.DataFrame({
                        'ds': pd.to_datetime([entry['timestamp'] for entry in data]),
                        'y': [entry['value'] for entry in data]
                    })
                    model = self._create_forecast_model()
                    model.fit(df)
                    self.forecast_models[metric] = model

            self.logger.info("Models trained successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to train models: {e}")
            return False

    def generate_report(self, days: int = None) -> Dict[str, Any]:
        """Generate a comprehensive historical analysis report"""
        try:
            days = days or self.analysis_window_days

            # Collect data
            self.collect_historical_data(days)

            # Analyze trends
            trends = {}
            for metric in ['cpu_usage', 'memory_usage', 'disk_usage', 'process_count', 'error_rates']:
                trends[metric] = self.analyze_trends(metric, days)

            # Predict issues
            issue_prediction = self.predict_system_issues()

            # Generate report
            report = {
                'timestamp': datetime.utcnow().isoformat(),
                'analysis_window_days': days,
                'trend_analysis': trends,
                'issue_predictions': issue_prediction,
                'recommendations': issue_prediction.get('overall_risk', {}).get('recommendations', [])
            }

            return report

        except Exception as e:
            self.logger.error(f"Failed to generate report: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }

    def log_historical_analysis(self, analysis_result: Dict[str, Any]):
        """Log historical analysis results"""
        try:
            # Log the analysis result
            self.logging_manager.log_metric(
                "historical_analysis",
                1,
                status=analysis_result.get('status', 'unknown'),
                risk_level=analysis_result.get('overall_risk', {}).get('overall_risk', 'unknown')
            )

            # Log individual metric predictions
            for metric, prediction in analysis_result.get('issue_predictions', {}).get('predictions', {}).items():
                self.logging_manager.log_metric(
                    f"prediction_{metric}",
                    prediction.get('issue_prediction', {}).get('risk_score', 0),
                    risk_level=prediction.get('issue_prediction', {}).get('risk_level', 'unknown'),
                    predicted_issues=','.join(prediction.get('issue_prediction', {}).get('predicted_issues', []))
                )

        except Exception as e:
            self.logger.error(f"Failed to log historical analysis: {e}")

    def run_periodic_analysis(self, interval_hours: int = 24):
        """Run periodic historical analysis"""
        try:
            while True:
                self.logger.info(f"Starting periodic historical analysis (interval: {interval_hours}h)")

                # Collect data and train models
                self.collect_historical_data()
                self.train_models()

                # Generate analysis report
                report = self.generate_report()

                # Log results
                self.log_historical_analysis(report)

                # Sleep until next analysis
                self.logger.info(f"Historical analysis completed. Next run in {interval_hours} hours.")
                time.sleep(interval_hours * 3600)

        except KeyboardInterrupt:
            self.logger.info("Periodic analysis stopped by user")
        except Exception as e:
            self.logger.error(f"Periodic analysis failed: {e}")

# Example usage
if __name__ == "__main__":
    # Initialize historical analyzer
    analyzer = HistoricalAnalyzer()

    # Collect historical data
    analyzer.collect_historical_data()

    # Train models
    analyzer.train_models()

    # Generate report
    report = analyzer.generate_report()
    print(json.dumps(report, indent=2, default=str))

    # Predict system issues
    predictions = analyzer.predict_system_issues()
    print(json.dumps(predictions, indent=2, default=str))

    # Run periodic analysis (in a separate thread in production)
    # analyzer.run_periodic_analysis(interval_hours=24)





