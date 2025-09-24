



"""
Document Classification ML Model

Uses scikit-learn for document classification with:
- TF-IDF feature extraction
- Logistic regression classifier
- Active learning capabilities
"""

import logging
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class DocumentClassifierModel:
    """Machine learning model for document classification"""

    def __init__(self, model_path: str = None):
        """
        Initialize document classifier model

        Args:
            model_path: Path to load/save model
        """
        self.model_path = model_path or "/tmp/document_classifier.pkl"
        self.model = None
        self.vectorizer = None
        self.is_trained = False

        # Try to load existing model
        if os.path.exists(self.model_path):
            try:
                self._load_model()
                logger.info("Loaded existing document classification model")
            except Exception as e:
                logger.warning(f"Failed to load model: {e}")
                self._initialize_model()

    def _initialize_model(self):
        """Initialize a new classification model"""
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.model = LogisticRegression(max_iter=1000)
        self.is_trained = False

    def _load_model(self):
        """Load model from disk"""
        with open(self.model_path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.vectorizer = data['vectorizer']
            self.is_trained = True

    def _save_model(self):
        """Save model to disk"""
        with open(self.model_path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'vectorizer': self.vectorizer
            }, f)

    def train(self, documents: List[str], labels: List[str]):
        """
        Train the classification model

        Args:
            documents: List of document texts
            labels: Corresponding classification labels
        """
        try:
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                documents, labels, test_size=0.2, random_state=42
            )

            # Create pipeline
            pipeline = Pipeline([
                ('tfidf', self.vectorizer),
                ('clf', self.model)
            ])

            # Train model
            pipeline.fit(X_train, y_train)

            # Evaluate
            score = pipeline.score(X_test, y_test)
            logger.info(f"Model trained with accuracy: {score:.2f}")

            # Save components
            self.model = pipeline.named_steps['clf']
            self.vectorizer = pipeline.named_steps['tfidf']
            self.is_trained = True
            self._save_model()

        except Exception as e:
            logger.error(f"Model training failed: {e}")
            raise

    def predict(self, document: str) -> Dict[str, Any]:
        """
        Predict document classification

        Args:
            document: Document text to classify

        Returns:
            Classification result with confidence
        """
        try:
            if not self.is_trained:
                logger.warning("Model not trained, using default classification")
                return {
                    "category": "unknown",
                    "confidence": 0.5
                }

            # Transform and predict
            features = self.vectorizer.transform([document])
            probabilities = self.model.predict_proba(features)
            prediction = self.model.predict(features)

            # Get confidence
            confidence = max(probabilities[0])

            return {
                "category": prediction[0],
                "confidence": float(confidence)
            }

        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {
                "category": "error",
                "confidence": 0.1,
                "error": str(e)
            }

    def update_with_feedback(self, document: str, correct_label: str):
        """
        Update model with user feedback

        Args:
            document: Document text
            correct_label: Correct classification label
        """
        try:
            # Simple online learning approach
            features = self.vectorizer.transform([document])
            self.model.partial_fit(features, [correct_label])

            # Save updated model
            self._save_model()
            logger.info("Model updated with user feedback")

        except Exception as e:
            logger.error(f"Model update failed: {e}")
            raise



