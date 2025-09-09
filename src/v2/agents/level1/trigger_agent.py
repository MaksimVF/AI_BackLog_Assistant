




"""
Trigger Agent for Level 1 Processing
"""

import logging
from typing import Dict, Any
from src.common.config import settings

logger = logging.getLogger(__name__)

class TriggerAgent:
    """Determines when to trigger Level 2 processing"""

    def __init__(self):
        # Default trigger thresholds
        self.thresholds = {
            'score': 0.7,  # Trigger if initial score > 0.7
            'batch_size': 10,  # Trigger if batch size > 10
            'time_interval': 3600,  # Trigger every hour (in seconds)
            'manual_override': True  # Allow manual triggering
        }

        # Track batch and time
        self.current_batch = []
        self.last_trigger_time = 0

    def check_conditions(self, classified_data: Dict[str, Any]) -> bool:
        """
        Check if Level 2 processing should be triggered

        Args:
            classified_data: Classified data from Content Classifier

        Returns:
            True if Level 2 should be triggered, False otherwise
        """
        try:
            metadata = classified_data.get('metadata', {})
            initial_score = metadata.get('initial_score', 0)

            # Check score threshold
            if initial_score > self.thresholds['score']:
                logger.info(f"Triggering Level 2: high score {initial_score}")
                return True

            # Add to current batch
            self.current_batch.append(classified_data)

            # Check batch size
            if len(self.current_batch) > self.thresholds['batch_size']:
                logger.info(f"Triggering Level 2: batch size {len(self.current_batch)} exceeded")
                return True

            # Check time interval (simplified for now)
            # In a real implementation, this would check actual time
            if self.thresholds['time_interval'] > 0:
                logger.info("Time-based triggering would be checked here")
                # Reset for demo purposes
                # self.last_trigger_time = time.time()

            return False

        except Exception as e:
            logger.error(f"Error checking trigger conditions: {e}")
            return False

    def manual_trigger(self) -> bool:
        """Manually trigger Level 2 processing"""
        if self.thresholds['manual_override']:
            logger.info("Manually triggering Level 2 processing")
            return True
        return False

    def get_batch(self) -> list:
        """Get current batch and clear it"""
        batch = self.current_batch.copy()
        self.current_batch = []
        return batch

    def update_thresholds(self, new_thresholds: Dict[str, Any]) -> None:
        """Update trigger thresholds"""
        self.thresholds.update(new_thresholds)
        logger.info(f"Updated trigger thresholds: {self.thresholds}")






