





from typing import Optional, List
from pydantic import BaseModel
import logging
import numpy as np

logger = logging.getLogger(__name__)

class SentimentAnalysis(BaseModel):
    """Sentiment analysis results"""
    sentiment: str  # positive, negative, neutral
    confidence: float
    sentiment_score: float  # Range from -1 (negative) to 1 (positive)
    emotion_details: Optional[dict] = None  # Detailed emotion analysis

class SentimentAnalyzer:
    """Analyzes sentiment of text input using advanced NLP techniques"""

    def __init__(self):
        # Initialize advanced sentiment analysis model
        # In a real implementation, we would load a pre-trained transformer model
        # For this example, we'll simulate an advanced model with enhanced keyword analysis
        self.emotion_keywords = {
            'joy': {'счастливый', 'радостный', 'восторженный', 'удовлетворенный'},
            'sadness': {'грустный', 'подавленный', 'унылый', 'печальный'},
            'anger': {'злой', 'раздраженный', 'сердитый', 'яростный'},
            'fear': {'боязливый', 'испуганный', 'тревожный', 'нервный'},
            'surprise': {'удивленный', 'пораженный', 'шокированный'},
            'disgust': {'отвратительный', 'мерзкий', 'противный'},
            'trust': {'доверчивый', 'уверенный', 'надежный'},
            'anticipation': {'ожидающий', 'надеющийся', 'предвкушающий'}
        }

        # Enhanced sentiment lexicon
        self.positive_keywords = {'хороший', 'отличный', 'прекрасный', 'счастливый', 'успешный',
                                'великолепный', 'замечательный', 'потрясающий', 'восхитительный'}
        self.negative_keywords = {'плохой', 'ужасный', 'грустный', 'проблема', 'кризис', 'стресс',
                                'кошмарный', 'отвратительный', 'ужасающий', 'бедственный'}

    def analyze(self, text: str) -> SentimentAnalysis:
        """
        Analyze sentiment of the given text using advanced techniques

        Args:
            text: Input text to analyze

        Returns:
            SentimentAnalysis: Analysis results
        """
        # Preprocess text
        words = self._preprocess_text(text)

        # Basic sentiment analysis
        positive_words = [word for word in words if word in self.positive_keywords]
        negative_words = [word for word in words if word in self.negative_keywords]

        # Calculate basic sentiment score
        basic_score = len(positive_words) - len(negative_words)

        # Enhanced emotion analysis
        emotion_scores = {}
        for emotion, keywords in self.emotion_keywords.items():
            emotion_words = [word for word in words if word in keywords]
            emotion_scores[emotion] = len(emotion_words)

        # Normalize emotion scores
        total_emotion = sum(emotion_scores.values())
        if total_emotion > 0:
            emotion_scores = {k: v / total_emotion for k, v in emotion_scores.items()}

        # Determine overall sentiment with emotion weighting
        sentiment_score = basic_score / (len(words) + 1)

        # Apply emotion weighting
        if 'joy' in emotion_scores:
            sentiment_score += emotion_scores['joy'] * 0.5
        if 'sadness' in emotion_scores:
            sentiment_score -= emotion_scores['sadness'] * 0.5
        if 'anger' in emotion_scores:
            sentiment_score -= emotion_scores['anger'] * 0.4
        if 'fear' in emotion_scores:
            sentiment_score -= emotion_scores['fear'] * 0.3

        # Clamp score to -1 to 1 range
        sentiment_score = min(1.0, max(-1.0, sentiment_score))

        # Determine sentiment category with enhanced thresholds
        if sentiment_score > 0.3:
            sentiment = 'positive'
            confidence = min(0.95, 0.7 + sentiment_score * 0.25)
        elif sentiment_score < -0.3:
            sentiment = 'negative'
            confidence = min(0.95, 0.7 - sentiment_score * 0.25)
        else:
            sentiment = 'neutral'
            confidence = 0.8 + (1 - abs(sentiment_score)) * 0.1

        logger.debug(f"Advanced sentiment analysis: {sentiment} ({sentiment_score:.2f}) for text: {text[:50]}...")

        return SentimentAnalysis(
            sentiment=sentiment,
            confidence=confidence,
            sentiment_score=sentiment_score,
            emotion_details=emotion_scores if emotion_scores else None
        )

    def _preprocess_text(self, text: str) -> List[str]:
        """Preprocess text for analysis"""
        # Convert to lowercase and split into words
        words = text.lower().split()

        # Remove punctuation and special characters
        words = [word.strip('.,!?;:()[]{}"\'') for word in words]

        # Remove empty strings
        words = [word for word in words if word]

        return words





