



"""
Content Classifier Agent for Level 1 Processing
"""

import logging
import re
from typing import Dict, Any, Optional
from src.v2.agents.level1.input_receiver import InputData

logger = logging.getLogger(__name__)

class ContentClassifierAgent:
    """Classifies content type, emotion, and provides initial scoring"""

    def __init__(self):
        # Content type patterns
        self.content_patterns = {
            'idea': [
                r'idea(s)?',
                r'suggestion(s)?',
                r'proposal(s)?',
                r'feature request(s)?',
                r'new feature(s)?',
                r'improvement(s)?'
            ],
            'bug': [
                r'bug(s)?',
                r'error(s)?',
                r'issue(s)?',
                r'problem(s)?',
                r'crash(es)?',
                r'not working',
                r'broken'
            ],
            'feedback': [
                r'feedback',
                r'comment(s)?',
                r'review(s)?',
                r'opinion(s)?',
                r'thought(s)?',
                r'suggestion(s)?'
            ],
            'question': [
                r'question(s)?',
                r'query|queries',
                r'asking',
                r'need help',
                r'how to',
                r'what is',
                r'why does'
            ]
        }

        # Emotion patterns
        self.emotion_patterns = {
            'positive': [
                r'good',
                r'great',
                r'excellent',
                r'happy',
                r'love',
                r'awesome',
                r'perfect',
                r'thank(s)?'
            ],
            'negative': [
                r'bad',
                r'terrible',
                r'hate',
                r'angry',
                r'problem',
                r'issue',
                r'bug',
                r'error',
                r'crash',
                r'broken',
                r'sad',
                r'unhappy'
            ]
        }

    def classify(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify content and provide initial analysis

        Args:
            processed_data: Data from modality processors

        Returns:
            Classified data with type, emotion, and score
        """
        try:
            content = processed_data.get('content', '')
            metadata = processed_data.get('metadata', {})

            # Classify content type
            content_type = self._classify_content_type(content)
            confidence = self._calculate_confidence(content, content_type)

            # Analyze emotion
            emotion = self._analyze_emotion(content)
            emotion_score = self._calculate_emotion_score(content, emotion)

            # Calculate initial score
            initial_score = self._calculate_initial_score(content_type, emotion_score)

            result = {
                'content': content,
                'metadata': {
                    **metadata,
                    'content_type': content_type,
                    'content_confidence': confidence,
                    'emotion': emotion,
                    'emotion_score': emotion_score,
                    'initial_score': initial_score
                }
            }

            logger.info(f"Classified content: type={content_type}, emotion={emotion}, score={initial_score}")
            return result

        except Exception as e:
            logger.error(f"Error classifying content: {e}")
            raise ValueError(f"Content classification failed: {e}")

    def _classify_content_type(self, content: str) -> str:
        """Classify content type based on patterns"""
        for content_type, patterns in self.content_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content.lower()):
                    return content_type
        return 'other'

    def _calculate_confidence(self, content: str, content_type: str) -> float:
        """Calculate confidence score for content classification"""
        if content_type == 'other':
            return 0.5  # Low confidence for unclassified

        # Count matches for the classified type
        matches = 0
        for pattern in self.content_patterns.get(content_type, []):
            if re.search(pattern, content.lower()):
                matches += 1

        # Simple confidence calculation
        return min(0.9, 0.5 + (matches * 0.1))

    def _analyze_emotion(self, content: str) -> str:
        """Analyze emotion based on patterns"""
        positive_score = sum(1 for pattern in self.emotion_patterns['positive']
                            if re.search(pattern, content.lower()))
        negative_score = sum(1 for pattern in self.emotion_patterns['negative']
                            if re.search(pattern, content.lower()))

        if positive_score > negative_score:
            return 'positive'
        elif negative_score > positive_score:
            return 'negative'
        else:
            return 'neutral'

    def _calculate_emotion_score(self, content: str, emotion: str) -> float:
        """Calculate emotion score"""
        if emotion == 'positive':
            return 0.7
        elif emotion == 'negative':
            return 0.3
        else:
            return 0.5

    def _calculate_initial_score(self, content_type: str, emotion_score: float) -> float:
        """Calculate initial score based on content type and emotion"""
        # Base scores by content type
        type_scores = {
            'idea': 0.8,
            'bug': 0.9,  # Bugs are high priority
            'feedback': 0.6,
            'question': 0.5,
            'other': 0.4
        }

        base_score = type_scores.get(content_type, 0.4)
        return (base_score + emotion_score) / 2



