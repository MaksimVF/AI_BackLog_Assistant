







from typing import List, Dict
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class TopicAnalysis(BaseModel):
    """Topic modeling results"""
    topics: List[str]  # List of detected topics
    topic_distribution: Dict[str, float]  # Topic distribution

class TopicModeler:
    """Performs basic topic modeling on text input"""

    def __init__(self):
        # In a real implementation, we would use LDA, NMF, or similar algorithms
        # For now, we'll use a simple keyword-based approach
        self.topic_keywords = {
            'work': ['работа', 'проект', 'коллега', 'начальник', 'офис'],
            'personal': ['семья', 'друг', 'отношения', 'личный', 'дом'],
            'finance': ['деньги', 'финансы', 'бюджет', 'инвестиции', 'зарплата'],
            'health': ['здоровье', 'стресс', 'медитация', 'упражнения', 'сон'],
            'technology': ['технология', 'программирование', 'компьютер', 'софт', 'интернет']
        }

    def analyze_topics(self, text: str) -> TopicAnalysis:
        """
        Analyze topics in the given text

        Args:
            text: Input text to analyze

        Returns:
            TopicAnalysis: Analysis results
        """
        words = set(text.lower().split())
        topic_scores = {}

        # Calculate topic scores based on keyword matches
        for topic, keywords in self.topic_keywords.items():
            matches = words.intersection(keywords)
            topic_scores[topic] = len(matches)

        # Normalize scores
        total_score = sum(topic_scores.values())
        if total_score == 0:
            # Default to general topic if no matches
            return TopicAnalysis(
                topics=['general'],
                topic_distribution={'general': 1.0}
            )

        topic_distribution = {topic: score / total_score for topic, score in topic_scores.items()}

        # Get top topics
        sorted_topics = sorted(topic_distribution.items(), key=lambda x: x[1], reverse=True)
        top_topics = [topic for topic, score in sorted_topics if score > 0.1]  # Minimum 10% threshold

        if not top_topics:
            top_topics = ['general']

        logger.debug(f"Topic analysis: {top_topics} for text: {text[:50]}...")

        return TopicAnalysis(
            topics=top_topics,
            topic_distribution=topic_distribution
        )







