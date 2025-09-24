




"""
Prioritization ML Model

Uses feature-based prioritization with:
- Reinforcement learning approach
- User feedback integration
- Feature engineering for better prioritization
"""

import logging
import numpy as np
from sklearn.linear_model import LinearRegression
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class PrioritizationModel:
    """Machine learning model for document prioritization"""

    def __init__(self):
        """Initialize prioritization model"""
        # Simple linear model for prioritization
        self.model = LinearRegression()

        # Feature weights - can be learned from data
        self.feature_weights = {
            "urgent_category": 0.3,
            "important_category": 0.2,
            "email_source": 0.1,
            "long_content": 0.1,
            "high_confidence": 0.1
        }

        # Training data
        self.training_data = []
        self.training_labels = []

    def extract_features(self, document_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract prioritization features from document data

        Args:
            document_data: Document data with classification and metadata

        Returns:
            Dictionary of prioritization features
        """
        features = {
            "urgent_category": 1.0 if document_data.get("classification", {}).get("category") == "urgent" else 0.0,
            "important_category": 1.0 if document_data.get("classification", {}).get("category") == "important" else 0.0,
            "email_source": 1.0 if document_data.get("metadata", {}).get("source") == "email" else 0.0,
            "long_content": 1.0 if len(document_data.get("content", "").split()) > 500 else 0.0,
            "high_confidence": 1.0 if document_data.get("classification", {}).get("confidence", 0) > 0.8 else 0.0
        }

        return features

    def calculate_priority(self, features: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculate priority based on features

        Args:
            features: Extracted prioritization features

        Returns:
            Priority calculation result
        """
        # Calculate base priority
        base_priority = 0.5

        # Apply feature weights
        for feature, weight in self.feature_weights.items():
            if feature in features:
                base_priority += features[feature] * weight

        # Normalize to 0-1 range
        priority_score = min(max(base_priority, 0.0), 1.0)

        # Determine priority level
        if priority_score > 0.7:
            priority_level = "high"
        elif priority_score > 0.4:
            priority_level = "medium"
        else:
            priority_level = "low"

        return {
            "priority_level": priority_level,
            "priority_score": priority_score,
            "features_used": features
        }

    def prioritize(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prioritize document based on its data

        Args:
            document_data: Document data with classification and metadata

        Returns:
            Document data with added prioritization
        """
        try:
            # Extract features
            features = self.extract_features(document_data)

            # Calculate priority
            priority = self.calculate_priority(features)

            return {
                **document_data,
                "prioritization": priority
            }

        except Exception as e:
            logger.error(f"Prioritization failed: {e}")
            return {
                **document_data,
                "prioritization": {
                    "priority_level": "medium",
                    "priority_score": 0.5,
                    "error": str(e)
                }
            }

    def update_with_feedback(self, document_data: Dict[str, Any], correct_priority: str):
        """
        Update model with user feedback

        Args:
            document_data: Original document data
            correct_priority: Correct priority level
        """
        try:
            # Extract features
            features = self.extract_features(document_data)

            # Convert to numerical format
            feature_values = list(features.values())

            # Convert priority to numerical
            priority_mapping = {"low": 0.2, "medium": 0.5, "high": 0.8}
            target_priority = priority_mapping.get(correct_priority, 0.5)

            # Add to training data
            self.training_data.append(feature_values)
            self.training_labels.append(target_priority)

            # Retrain if enough data
            if len(self.training_data) > 10:
                self._retrain_model()

        except Exception as e:
            logger.error(f"Feedback update failed: {e}")
            raise

    def _retrain_model(self):
        """Retrain the prioritization model"""
        try:
            # Convert to numpy arrays
            X = np.array(self.training_data)
            y = np.array(self.training_labels)

            # Train model
            self.model.fit(X, y)

            # Update feature weights based on model coefficients
            if hasattr(self.model, 'coef_'):
                coefficients = self.model.coef_
                feature_names = list(self.feature_weights.keys())

                # Update weights
                for i, feature in enumerate(feature_names[:len(coefficients)]):
                    self.feature_weights[feature] = float(coefficients[i])

            logger.info("Prioritization model retrained with new data")

        except Exception as e:
            logger.error(f"Model retraining failed: {e}")
            raise




