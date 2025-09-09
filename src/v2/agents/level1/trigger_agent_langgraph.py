
"""
Refactored Trigger Agent using LangGraph for complex calculations
"""

import logging
from typing import Dict, Any, TypedDict, List, Callable
from datetime import datetime, timedelta
from langgraph.graph import StateGraph
from src.common.config import settings

logger = logging.getLogger(__name__)

class TriggerContext(TypedDict):
    """Context data for trigger calculations"""
    classified_data: Dict[str, Any]
    current_batch_size: int
    last_trigger_time: float
    thresholds: Dict[str, Any]
    calculation_results: Dict[str, Any]
    trigger_decision: bool

class LangGraphTriggerAgent:
    """Trigger Agent using LangGraph for complex decision making"""

    def __init__(self):
        # Default trigger thresholds
        self.thresholds = {
            'score': 0.6,  # Trigger if initial score > 0.6 (lower for hybrid classifier)
            'batch_size': 10,  # Trigger if batch size > 10
            'time_interval': 3600,  # Trigger every hour (in seconds)
            'manual_override': True,  # Allow manual triggering
            'score_weight': 0.7,  # Higher score weight
            'batch_weight': 0.15,
            'time_weight': 0.05,
            'complexity_threshold': 0.4  # Lower threshold for hybrid classifier
        }

        # Track batch and time
        self.current_batch = []
        self.last_trigger_time = 0

        # Initialize LangGraph
        self.graph = self._build_trigger_graph()

    def _build_trigger_graph(self) -> StateGraph:
        """Build the LangGraph for trigger calculations using StateGraph"""

        # Define the graph with our trigger context as state
        graph = StateGraph(TriggerContext)

        # Add nodes with their respective functions
        # Each node will receive the current state and return updated state
        graph.add_node("score_calculator", self._calculate_score_factor)
        graph.add_node("batch_calculator", self._calculate_batch_factor)
        graph.add_node("time_calculator", self._calculate_time_factor)
        graph.add_node("complexity_analyzer", self._analyze_complexity)
        graph.add_node("aggregation_node", self._aggregate_factors)
        graph.add_node("decision_node", self._make_trigger_decision)

        # For LangGraph, we need to chain the nodes sequentially
        # since parallel execution requires more complex setup
        graph.add_edge("score_calculator", "batch_calculator")
        graph.add_edge("batch_calculator", "time_calculator")
        graph.add_edge("time_calculator", "complexity_analyzer")
        graph.add_edge("complexity_analyzer", "aggregation_node")
        graph.add_edge("aggregation_node", "decision_node")

        # Set entry point and final node
        graph.set_entry_point("score_calculator")
        graph.set_finish_point("decision_node")

        return graph

    def _calculate_score_factor(self, state: TriggerContext) -> TriggerContext:
        """Calculate score-based trigger factor"""
        try:
            metadata = state['classified_data'].get('metadata', {})
            initial_score = metadata.get('initial_score', 0)

            logger.info(f"Initial score from data: {initial_score}")

            # Normalize score to 0-1 range
            score_factor = min(max(initial_score, 0), 1)

            # Apply weight
            weighted_score = score_factor * self.thresholds['score_weight']

            logger.info(f"Score factor: {score_factor:.3f}, Weighted: {weighted_score:.3f}")

            # Update state with calculation result
            state['calculation_results']['score_factor'] = weighted_score
            return state

        except Exception as e:
            logger.error(f"Error calculating score factor: {e}")
            state['calculation_results']['score_factor'] = 0.0
            return state

    def _calculate_batch_factor(self, state: TriggerContext) -> TriggerContext:
        """Calculate batch-based trigger factor"""
        try:
            batch_size = state['current_batch_size']

            # Normalize batch size to 0-1 range
            max_batch = self.thresholds['batch_size']
            batch_factor = min(max(batch_size / max_batch, 0), 1)

            # Apply weight
            weighted_batch = batch_factor * self.thresholds['batch_weight']

            # Update state
            state['calculation_results']['batch_factor'] = weighted_batch
            return state

        except Exception as e:
            logger.error(f"Error calculating batch factor: {e}")
            state['calculation_results']['batch_factor'] = 0.0
            return state

    def _calculate_time_factor(self, state: TriggerContext) -> TriggerContext:
        """Calculate time-based trigger factor"""
        try:
            current_time = datetime.now().timestamp()
            last_trigger = state['last_trigger_time']
            time_interval = self.thresholds['time_interval']

            if last_trigger == 0:
                # First run - don't trigger on time
                time_factor = 0.0
            else:
                time_since_last = current_time - last_trigger
                # Normalize time factor to 0-1 range
                time_factor = min(max(time_since_last / time_interval, 0), 1)

            # Apply weight
            weighted_time = time_factor * self.thresholds['time_weight']

            # Update state
            state['calculation_results']['time_factor'] = weighted_time
            return state

        except Exception as e:
            logger.error(f"Error calculating time factor: {e}")
            state['calculation_results']['time_factor'] = 0.0
            return state

    def _analyze_complexity(self, state: TriggerContext) -> TriggerContext:
        """Analyze complexity of the classified data"""
        try:
            classified_data = state['classified_data']

            # Handle different content formats
            if isinstance(classified_data, dict):
                if 'content' in classified_data:
                    content = classified_data['content']
                    if isinstance(content, dict):
                        text = content.get('text', '')
                    else:
                        text = str(content)
                else:
                    text = str(classified_data)
            else:
                text = str(classified_data)

            # Simple complexity metrics (can be enhanced with NLP)
            word_count = len(text.split())

            # Get metadata if available
            metadata = classified_data.get('metadata', {})
            entity_count = 0
            relationship_count = 0

            if 'entities' in metadata:
                entity_count = len(metadata['entities'])
            if 'relationships' in metadata:
                relationship_count = len(metadata['relationships'])

            # Calculate complexity score (0-1 range)
            max_words = 1000  # Example threshold
            complexity = min((word_count / max_words) * 0.4 +
                           (entity_count / 50) * 0.3 +
                           (relationship_count / 20) * 0.3, 1)

            # Apply weight from thresholds
            remaining_weight = 1 - sum([
                self.thresholds['score_weight'],
                self.thresholds['batch_weight'],
                self.thresholds['time_weight']
            ])

            weighted_complexity = complexity * remaining_weight

            # Update state
            state['calculation_results']['complexity_factor'] = weighted_complexity
            return state

        except Exception as e:
            logger.error(f"Error analyzing complexity: {e}")
            state['calculation_results']['complexity_factor'] = 0.0
            return state

    def _aggregate_factors(self, state: TriggerContext) -> TriggerContext:
        """Aggregate all factors into a final trigger score"""
        try:
            factors = state['calculation_results']
            total_score = sum(factors.values())

            # Normalize to 0-1 range
            final_score = min(max(total_score, 0), 1)

            # Update state
            state['calculation_results']['final_score'] = final_score
            return state

        except Exception as e:
            logger.error(f"Error aggregating factors: {e}")
            state['calculation_results']['final_score'] = 0.0
            return state

    def _make_trigger_decision(self, state: TriggerContext) -> TriggerContext:
        """Make final trigger decision"""
        try:
            final_score = state['calculation_results'].get('final_score', 0.0)
            complexity_threshold = self.thresholds['complexity_threshold']

            # Log calculation details
            logger.info(f"Trigger calculation results: {state['calculation_results']}")
            logger.info(f"Final score: {final_score:.3f}, Threshold: {complexity_threshold}")

            # Decision logic
            should_trigger = final_score >= complexity_threshold

            if should_trigger:
                logger.info(f"✅ TRIGGERING Level 2: complexity score {final_score:.3f} >= {complexity_threshold}")
            else:
                logger.info(f"❌ NOT triggering: complexity score {final_score:.3f} < {complexity_threshold}")

            # Store the decision in the state
            state['trigger_decision'] = should_trigger
            return state

        except Exception as e:
            logger.error(f"Error making trigger decision: {e}")
            state['trigger_decision'] = False
            return state

    def check_conditions(self, classified_data: Dict[str, Any]) -> bool:
        """
        Check if Level 2 processing should be triggered using LangGraph

        Args:
            classified_data: Classified data from Content Classifier

        Returns:
            True if Level 2 should be triggered, False otherwise
        """
        try:
            # Prepare context
            context: TriggerContext = {
                'classified_data': classified_data,
                'current_batch_size': len(self.current_batch),
                'last_trigger_time': self.last_trigger_time,
                'thresholds': self.thresholds,
                'calculation_results': {}
            }

            # Add to current batch
            self.current_batch.append(classified_data)

            # Execute LangGraph workflow
            # The graph will return the final state after all processing
            compiled_graph = self.graph.compile()
            final_state = compiled_graph.invoke(context)

            # The decision is made in the final state by the decision_node
            # We need to extract the trigger decision from the final state
            should_trigger = final_state.get('trigger_decision', False)

            # Update last trigger time if triggered
            if should_trigger:
                self.last_trigger_time = datetime.now().timestamp()

            return should_trigger

        except Exception as e:
            logger.error(f"Error checking trigger conditions: {e}")
            return False

    def manual_trigger(self) -> bool:
        """Manually trigger Level 2 processing"""
        if self.thresholds['manual_override']:
            logger.info("Manually triggering Level 2 processing")
            self.last_trigger_time = datetime.now().timestamp()
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

        # Update weights in the graph nodes
        # This would be more sophisticated in a real implementation
        self.graph = self._build_trigger_graph()
