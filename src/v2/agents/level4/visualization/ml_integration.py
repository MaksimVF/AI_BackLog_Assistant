









"""
Machine Learning Integration

Integrates machine learning capabilities with visualization.
"""

import logging
from typing import List, Dict, Any, Optional
from crewai import Agent
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import numpy as np

logger = logging.getLogger(__name__)

class MachineLearningIntegration:
    """
    Integrates machine learning capabilities with visualization.
    """

    def __init__(self):
        """
        Initialize machine learning integration with CrewAI agent.
        """
        # Initialize CrewAI agent for machine learning integration
        self.agent = Agent(
            name="MachineLearningIntegration",
            role="Machine learning integration for visualization",
            goal="""
                Integrate machine learning capabilities with visualization.
                Provide anomaly detection, clustering, and predictive analytics.
            """,
            backstory="""
                You are a machine learning integration agent that uses
                advanced ML algorithms to enhance visualization.
            """,
            tools=[],
            verbose=True
        )

    def detect_anomalies(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Detect anomalies in data using machine learning.

        Args:
            data: Data to analyze

        Returns:
            Anomaly detection results
        """
        try:
            # Prepare data for anomaly detection
            features = self._prepare_features(data)

            # Use Isolation Forest for anomaly detection
            model = IsolationForest(contamination=0.1, random_state=42)
            model.fit(features)

            # Predict anomalies
            anomalies = model.predict(features)
            anomaly_scores = model.decision_function(features)

            # Identify anomalies
            anomaly_results = []
            for i, (item, is_anomaly, score) in enumerate(zip(data, anomalies, anomaly_scores)):
                if is_anomaly == -1:
                    anomaly_results.append({
                        "item": item,
                        "anomaly_score": score,
                        "is_anomaly": True
                    })

            return {
                "anomalies": anomaly_results,
                "anomaly_count": len(anomaly_results),
                "metadata": {
                    "contextual_insights": "Anomaly detection with machine learning",
                    "model_type": "IsolationForest",
                    "contamination": 0.1
                }
            }

        except Exception as e:
            logger.error(f"Anomaly detection failed: {e}")
            raise

    def _prepare_features(self, data: List[Dict[str, Any]]) -> np.ndarray:
        """
        Prepare features from data for machine learning.

        Args:
            data: Data to prepare

        Returns:
            Feature array
        """
        # Extract numerical features
        features = []
        for item in data:
            feature_vector = []
            for key, value in item.items():
                if isinstance(value, (int, float)):
                    feature_vector.append(value)
                elif isinstance(value, str):
                    # Convert string to numerical value (simplified)
                    feature_vector.append(len(value))
                else:
                    feature_vector.append(0)

            # Ensure consistent feature length
            if len(feature_vector) < 5:
                feature_vector.extend([0] * (5 - len(feature_vector)))

            features.append(feature_vector[:5])  # Limit to 5 features

        return np.array(features)

    def cluster_data(self, data: List[Dict[str, Any]], num_clusters: int = 3) -> Dict[str, Any]:
        """
        Cluster data using machine learning.

        Args:
            data: Data to cluster
            num_clusters: Number of clusters

        Returns:
            Clustering results
        """
        try:
            # Prepare data for clustering
            features = self._prepare_features(data)

            # Use KMeans for clustering
            model = KMeans(n_clusters=num_clusters, random_state=42)
            model.fit(features)

            # Assign clusters
            clusters = model.predict(features)
            cluster_centers = model.cluster_centers_

            # Organize results
            clustered_data = []
            for i, (item, cluster) in enumerate(zip(data, clusters)):
                clustered_data.append({
                    "item": item,
                    "cluster": cluster,
                    "distance_to_center": np.linalg.norm(features[i] - cluster_centers[cluster])
                })

            return {
                "clusters": clustered_data,
                "cluster_centers": cluster_centers.tolist(),
                "num_clusters": num_clusters,
                "metadata": {
                    "contextual_insights": "Data clustering with machine learning",
                    "model_type": "KMeans",
                    "num_clusters": num_clusters
                }
            }

        except Exception as e:
            logger.error(f"Clustering failed: {e}")
            raise

    def predict_trends(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Predict trends using machine learning.

        Args:
            data: Data to analyze

        Returns:
            Trend prediction results
        """
        try:
            # Prepare data for trend prediction
            features = self._prepare_features(data)

            # Use linear regression for trend prediction
            model = LinearRegression()
            model.fit(np.arange(len(features)).reshape(-1, 1), features)

            # Predict future trends
            future_steps = 5
            future_predictions = model.predict(np.arange(len(features), len(features) + future_steps).reshape(-1, 1))

            return {
                "trend_prediction": future_predictions.tolist(),
                "future_steps": future_steps,
                "metadata": {
                    "contextual_insights": "Trend prediction with machine learning",
                    "model_type": "LinearRegression",
                    "future_steps": future_steps
                }
            }

        except Exception as e:
            logger.error(f"Trend prediction failed: {e}")
            raise

    def analyze_sentiment(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze sentiment in text data using machine learning.

        Args:
            data: Data to analyze

        Returns:
            Sentiment analysis results
        """
        try:
            # Extract text data
            text_data = []
            for item in data:
                for key, value in item.items():
                    if isinstance(value, str):
                        text_data.append(value)

            # Use simple sentiment analysis (placeholder for actual implementation)
            sentiment_results = []
            for text in text_data:
                sentiment = self._analyze_text_sentiment(text)
                sentiment_results.append({
                    "text": text,
                    "sentiment": sentiment,
                    "sentiment_score": 0.5 if sentiment == "neutral" else 0.7 if sentiment == "positive" else 0.3
                })

            return {
                "sentiment_analysis": sentiment_results,
                "metadata": {
                    "contextual_insights": "Sentiment analysis with machine learning",
                    "model_type": "SimpleSentiment",
                    "texts_analyzed": len(text_data)
                }
            }

        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            raise

    def _analyze_text_sentiment(self, text: str) -> str:
        """
        Analyze sentiment of text (simplified implementation).

        Args:
            text: Text to analyze

        Returns:
            Sentiment (positive, neutral, negative)
        """
        # Simple sentiment analysis (placeholder)
        if "security" in text.lower() or "vulnerability" in text.lower():
            return "negative"
        elif "update" in text.lower() or "improve" in text.lower():
            return "positive"
        else:
            return "neutral"

    def generate_ml_insights(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate comprehensive machine learning insights.

        Args:
            data: Data to analyze

        Returns:
            Machine learning insights
        """
        try:
            # Run multiple ML analyses
            anomaly_results = self.detect_anomalies(data)
            cluster_results = self.cluster_data(data)
            trend_results = self.predict_trends(data)
            sentiment_results = self.analyze_sentiment(data)

            # Combine insights
            ml_insights = {
                "anomalies": anomaly_results["anomalies"],
                "clusters": cluster_results["clusters"],
                "trend_prediction": trend_results["trend_prediction"],
                "sentiment_analysis": sentiment_results["sentiment_analysis"],
                "metadata": {
                    "contextual_insights": "Comprehensive machine learning insights",
                    "analyses_performed": ["anomaly_detection", "clustering", "trend_prediction", "sentiment_analysis"]
                }
            }

            return ml_insights

        except Exception as e:
            logger.error(f"ML insights generation failed: {e}")
            raise

    def get_recommendations(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get recommendations based on machine learning analysis.

        Args:
            data: Data to analyze

        Returns:
            Recommendations
        """
        try:
            # Run ML analysis
            ml_insights = self.generate_ml_insights(data)

            # Generate recommendations
            recommendations = []

            # Anomaly recommendations
            if ml_insights["anomalies"]:
                recommendations.append(f"Investigate {len(ml_insights['anomalies'])} potential anomalies")

            # Cluster recommendations
            if ml_insights["clusters"]:
                recommendations.append(f"Explore {len(set(item['cluster'] for item in ml_insights['clusters']))} distinct clusters")

            # Trend recommendations
            if ml_insights["trend_prediction"]:
                recommendations.append("Monitor predicted trends for future planning")

            # Sentiment recommendations
            if ml_insights["sentiment_analysis"]:
                negative_sentiments = [item for item in ml_insights["sentiment_analysis"] if item["sentiment"] == "negative"]
                if negative_sentiments:
                    recommendations.append(f"Address {len(negative_sentiments)} negative sentiment items")

            return {
                "recommendations": recommendations,
                "metadata": {
                    "contextual_insights": "Recommendations based on machine learning analysis",
                    "recommendation_count": len(recommendations)
                }
            }

        except Exception as e:
            logger.error(f"Recommendations generation failed: {e}")
            raise







