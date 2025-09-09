






from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class TemporalPattern(BaseModel):
    """Represents a detected temporal pattern"""
    pattern_type: str  # e.g., 'recurring', 'trend', 'anomaly'
    description: str
    frequency: Optional[str] = None  # e.g., 'daily', 'weekly'
    confidence: float

class TemporalAnalyzer:
    """Analyzes temporal patterns in user inputs"""

    def __init__(self, memory):
        self.memory = memory

    def analyze_patterns(self, user_id: str, current_text: str) -> List[TemporalPattern]:
        """
        Analyze temporal patterns for a user

        Args:
            user_id: User identifier
            current_text: Current input text

        Returns:
            List of detected temporal patterns
        """
        patterns = []

        # Get user history
        history = self.memory.query_user_history(user_id, limit=50)

        if not history:
            return patterns

        # Convert to chronological order
        history.sort(key=lambda x: x.get('timestamp', datetime.min))

        # Check for recurring patterns
        recurring_pattern = self._detect_recurring_patterns(history, current_text)
        if recurring_pattern:
            patterns.append(recurring_pattern)

        # Check for trends
        trend_pattern = self._detect_trends(history)
        if trend_pattern:
            patterns.append(trend_pattern)

        # Check for anomalies
        anomaly_pattern = self._detect_anomalies(history, current_text)
        if anomaly_pattern:
            patterns.append(anomaly_pattern)

        return patterns

    def _detect_recurring_patterns(self, history: List[Dict], current_text: str) -> Optional[TemporalPattern]:
        """Detect recurring patterns in user inputs"""
        # Simple implementation: check if similar text appears regularly
        similar_items = [item for item in history if self._text_similarity(item['content'], current_text) > 0.7]

        if len(similar_items) < 2:
            return None

        # Check time intervals between similar items
        time_intervals = []
        for i in range(1, len(similar_items)):
            prev_time = similar_items[i-1].get('timestamp', datetime.min)
            curr_time = similar_items[i].get('timestamp', datetime.min)
            if prev_time and curr_time:
                delta = curr_time - prev_time
                time_intervals.append(delta.total_seconds())

        # Check if intervals are consistent
        if len(time_intervals) < 2:
            return None

        avg_interval = sum(time_intervals) / len(time_intervals)
        interval_variance = sum((x - avg_interval) ** 2 for x in time_intervals) / len(time_intervals)

        # If intervals are consistent (low variance), we have a recurring pattern
        if interval_variance < (avg_interval * 0.3):  # 30% variance threshold
            # Determine frequency
            if avg_interval < 3600 * 24:  # Less than a day
                frequency = 'daily'
            elif avg_interval < 3600 * 24 * 7:  # Less than a week
                frequency = 'weekly'
            else:
                frequency = 'monthly'

            return TemporalPattern(
                pattern_type='recurring',
                description=f'Recurring pattern detected every {frequency}',
                frequency=frequency,
                confidence=0.85
            )

        return None

    def _detect_trends(self, history: List[Dict]) -> Optional[TemporalPattern]:
        """Detect trends in user inputs"""
        # Simple implementation: check if sentiment is trending up or down
        sentiments = []
        for item in history:
            if 'sentiment' in item:
                sentiments.append(item['sentiment'])

        if len(sentiments) < 5:
            return None

        # Check if there's a consistent trend
        positive_trend = 0
        negative_trend = 0

        for i in range(1, len(sentiments)):
            if sentiments[i] > sentiments[i-1]:
                positive_trend += 1
            elif sentiments[i] < sentiments[i-1]:
                negative_trend += 1

        if positive_trend > negative_trend + 2:
            return TemporalPattern(
                pattern_type='trend',
                description='Positive sentiment trend detected',
                confidence=0.8
            )
        elif negative_trend > positive_trend + 2:
            return TemporalPattern(
                pattern_type='trend',
                description='Negative sentiment trend detected',
                confidence=0.8
            )

        return None

    def _detect_anomalies(self, history: List[Dict], current_text: str) -> Optional[TemporalPattern]:
        """Detect anomalies in user inputs"""
        # Simple implementation: check if current text is very different from history
        if not history:
            return None

        # Calculate average similarity to history
        similarities = []
        for item in history:
            if 'content' in item:
                similarities.append(self._text_similarity(item['content'], current_text))

        if not similarities:
            return None

        avg_similarity = sum(similarities) / len(similarities)

        # If current text is very different from average, it's an anomaly
        if avg_similarity < 0.3:  # Less than 30% similarity
            return TemporalPattern(
                pattern_type='anomaly',
                description='Unusual input detected compared to user history',
                confidence=0.9
            )

        return None

    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity (placeholder for real implementation)"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        intersection = words1.intersection(words2)
        return len(intersection) / max(1, len(words1.union(words2)))






