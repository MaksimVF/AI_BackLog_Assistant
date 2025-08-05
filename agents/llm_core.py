

"""
LLM Core - Central module for handling agent commands, reflections, self-improvement,
decision-making, and coordination.

This module serves as the central intelligence of the AI system, coordinating all
agent activities and providing higher-level cognitive functions.
"""

from typing import Dict, Any, List, Optional, Union, Literal
from pydantic import BaseModel
from datetime import datetime
import logging
import json
import uuid

# Import existing components - handle imports gracefully
try:
    from memory.weaviate_client import WeaviateMemory
    from memory.memory_manager import MemoryManager
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False
    logging.warning("Memory components not available - running in lightweight mode")

try:
    from agents.reflection_agent import ReflectionAgent, ReflectionInput, ReflectionOutput
    REFLECTION_AVAILABLE = True
except ImportError:
    REFLECTION_AVAILABLE = False
    logging.warning("Reflection agent not available - running in lightweight mode")

try:
    from agents.pipeline_coordinator_agent import PipelineCoordinatorAgent
    PIPELINE_AVAILABLE = True
except ImportError:
    PIPELINE_AVAILABLE = False
    logging.warning("Pipeline coordinator not available - running in lightweight mode")

try:
    from agents.analyzers.context_classifier import ContextClassifier
    from agents.analyzers.intent_identifier import IntentIdentifier
    ANALYZERS_AVAILABLE = True
except ImportError:
    ANALYZERS_AVAILABLE = False
    logging.warning("Analyzer components not available - running in lightweight mode")

logger = logging.getLogger(__name__)

class LLMCoreConfig(BaseModel):
    """Configuration for LLM Core"""
    enable_memory: bool = True
    enable_reflection: bool = True
    enable_self_improvement: bool = True
    max_history_length: int = 100
    debug_mode: bool = False

class AgentCommand(BaseModel):
    """Standard format for agent commands"""
    command_type: Literal['process', 'analyze', 'route', 'reflect', 'improve', 'coordinate']
    agent_id: str
    payload: Dict[str, Any]
    priority: Literal['high', 'medium', 'low'] = 'medium'
    timestamp: str = datetime.utcnow().isoformat()

class AgentResponse(BaseModel):
    """Standard format for agent responses"""
    status: Literal['success', 'failure', 'partial']
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str = datetime.utcnow().isoformat()

class SelfImprovementPlan(BaseModel):
    """Plan for self-improvement based on reflections"""
    areas_for_improvement: List[str]
    recommended_actions: List[str]
    priority: Literal['high', 'medium', 'low']
    deadline: Optional[str] = None

class LLMCore:
    """
    Central LLM Core that handles all agent commands, reflections, self-improvement,
    decision-making, and coordination.
    """

    def __init__(self, config: Optional[LLMCoreConfig] = None):
        """
        Initialize LLM Core with configuration.

        Args:
            config: Configuration for LLM Core
        """
        self.config = config or LLMCoreConfig()
        self.session_id = str(uuid.uuid4())
        self.command_history = []
        self.performance_metrics = {
            'total_commands': 0,
            'success_count': 0,
            'failure_count': 0,
            'avg_processing_time': 0.0
        }

        # Initialize components based on availability
        self.memory = MemoryManager() if self.config.enable_memory and MEMORY_AVAILABLE else None
        self.reflection_agent = ReflectionAgent() if self.config.enable_reflection and REFLECTION_AVAILABLE else None
        self.pipeline_coordinator = PipelineCoordinatorAgent() if PIPELINE_AVAILABLE else None

        # Initialize core components
        self._initialize_components()

    def _initialize_components(self):
        """Initialize all core components"""
        logger.info(f"Initializing LLM Core (Session: {self.session_id})")
        if self.config.debug_mode:
            logger.setLevel(logging.DEBUG)

    def process_command(self, command: AgentCommand) -> AgentResponse:
        """
        Process an agent command through the LLM Core.

        Args:
            command: AgentCommand to process

        Returns:
            AgentResponse with results
        """
        start_time = datetime.utcnow()
        self.performance_metrics['total_commands'] += 1

        try:
            # Log the command
            self._log_command(command)

            # Route command to appropriate handler
            if command.command_type == 'process':
                result = self._handle_process_command(command)
            elif command.command_type == 'analyze':
                result = self._handle_analyze_command(command)
            elif command.command_type == 'route':
                result = self._handle_route_command(command)
            elif command.command_type == 'reflect':
                result = self._handle_reflect_command(command)
            elif command.command_type == 'improve':
                result = self._handle_improve_command(command)
            elif command.command_type == 'coordinate':
                result = self._handle_coordinate_command(command)
            else:
                raise ValueError(f"Unknown command type: {command.command_type}")

            # Update metrics
            self.performance_metrics['success_count'] += 1

            return AgentResponse(
                status='success',
                result=result,
                timestamp=datetime.utcnow().isoformat()
            )

        except Exception as e:
            self.performance_metrics['failure_count'] += 1
            logger.error(f"Error processing command: {e}")

            return AgentResponse(
                status='failure',
                error=str(e),
                timestamp=datetime.utcnow().isoformat()
            )
        finally:
            # Calculate processing time
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            self.performance_metrics['avg_processing_time'] = (
                (self.performance_metrics['avg_processing_time'] * (self.performance_metrics['total_commands'] - 1) + processing_time)
                / self.performance_metrics['total_commands']
            )

    def _log_command(self, command: AgentCommand):
        """Log a command to history"""
        if len(self.command_history) >= self.config.max_history_length:
            self.command_history.pop(0)
        self.command_history.append({
            'command': command.dict(),
            'timestamp': datetime.utcnow().isoformat()
        })

    def _handle_process_command(self, command: AgentCommand) -> Dict[str, Any]:
        """Handle process commands"""
        payload = command.payload
        input_type = payload.get('input_type', 'text')
        data = payload.get('data')

        if not data:
            raise ValueError("No data provided for processing")

        # Use pipeline coordinator for processing if available
        if self.pipeline_coordinator:
            result = self.pipeline_coordinator.process(input_type, data)
        else:
            # Fallback simple processing
            result = {
                "input_type": input_type,
                "processed_data": data,
                "status": "processed_without_pipeline",
                "message": "Pipeline coordinator not available, using fallback processing"
            }

        # Store in memory if enabled
        if self.memory:
            try:
                self.memory.store_processing_result(
                    session_id=self.session_id,
                    input_type=input_type,
                    input_data=data,
                    result=result
                )
            except Exception as e:
                logger.warning(f"Failed to store in memory: {e}")

        return result

    def _handle_analyze_command(self, command: AgentCommand) -> Dict[str, Any]:
        """Handle analyze commands"""
        payload = command.payload
        text = payload.get('text')

        if not text:
            raise ValueError("No text provided for analysis")

        # Use reflection agent for analysis if available
        if self.reflection_agent:
            reflection_input = ReflectionInput(content=text)
            analysis_result = self.reflection_agent.reflect(reflection_input)

            # Store analysis in memory
            if self.memory:
                try:
                    self.memory.store_analysis_result(
                        session_id=self.session_id,
                        input_text=text,
                        analysis=analysis_result.dict()
                    )
                except Exception as e:
                    logger.warning(f"Failed to store analysis in memory: {e}")

            return analysis_result.dict()
        else:
            # Fallback simple analysis - use basic analyzers if available
            try:
                from agents.analyzers.context_classifier import ContextClassifier
                from agents.analyzers.intent_identifier import IntentIdentifier

                # Simple fallback analysis
                context_classifier = ContextClassifier()
                intent_identifier = IntentIdentifier()

                context_analysis = context_classifier.classify(text)
                intent_analysis = intent_identifier.identify(text)

                return {
                    "context": context_analysis.context,
                    "intent": intent_analysis.intent_type,
                    "confidence": (context_analysis.confidence + intent_analysis.confidence) / 2,
                    "status": "analyzed_with_fallback",
                    "message": "Reflection agent not available, using fallback analysis"
                }
            except ImportError:
                # Minimal fallback
                return {
                    "context": "неизвестно",
                    "intent": "неизвестно",
                    "confidence": 0.5,
                    "status": "analyzed_with_minimal_fallback",
                    "message": "All analysis components not available, using minimal fallback"
                }

    def _handle_route_command(self, command: AgentCommand) -> Dict[str, Any]:
        """Handle routing commands"""
        payload = command.payload
        text = payload.get('text')

        if not text:
            raise ValueError("No text provided for routing")

        # Use pipeline coordinator for routing if available
        if self.pipeline_coordinator:
            routing_result = self.pipeline_coordinator.analyze_and_route(text)
            return routing_result.dict()
        else:
            # Fallback simple routing
            text_lower = text.lower()
            if "договор" in text_lower or "контракт" in text_lower:
                next_agent = "contract_analyzer"
            elif "отчёт" in text_lower or "репорт" in text_lower:
                next_agent = "report_analyzer"
            elif "письмо" in text_lower or "email" in text_lower:
                next_agent = "email_analyzer"
            else:
                next_agent = "general_analyzer"

            return {
                "next_agent": next_agent,
                "priority": "medium",
                "reasoning": "Fallback routing based on keywords",
                "status": "routed_with_fallback",
                "message": "Pipeline coordinator not available, using fallback routing"
            }

    def _handle_reflect_command(self, command: AgentCommand) -> Dict[str, Any]:
        """Handle reflection commands"""
        payload = command.payload
        text = payload.get('text')

        if not text:
            raise ValueError("No text provided for reflection")

        if self.reflection_agent:
            # Perform reflection using the reflection agent
            reflection_input = ReflectionInput(content=text)
            reflection_result = self.reflection_agent.reflect(reflection_input)

            # Generate self-improvement plan if needed
            improvement_plan = self._generate_improvement_plan(reflection_result)

            return {
                'reflection': reflection_result.dict(),
                'improvement_plan': improvement_plan.dict() if improvement_plan else None
            }
        else:
            # Fallback reflection - use basic analysis
            try:
                from agents.analyzers.context_classifier import ContextClassifier
                from agents.analyzers.intent_identifier import IntentIdentifier

                context_classifier = ContextClassifier()
                intent_identifier = IntentIdentifier()

                context_analysis = context_classifier.classify(text)
                intent_analysis = intent_identifier.identify(text)

                # Simple fallback reflection
                fallback_reflection = {
                    "context": context_analysis.context,
                    "intent": intent_analysis.intent_type,
                    "confidence": (context_analysis.confidence + intent_analysis.confidence) / 2,
                    "reasoning": f"Context: {context_analysis.context}, Intent: {intent_analysis.intent_type}",
                    "status": "reflected_with_fallback",
                    "message": "Reflection agent not available, using fallback reflection"
                }

                # Generate simple improvement plan
                improvement_plan = {
                    "areas_for_improvement": ["Enhance reflection capabilities"],
                    "recommended_actions": ["Integrate full reflection agent"],
                    "priority": "medium",
                    "status": "improvement_plan_with_fallback"
                }

                return {
                    'reflection': fallback_reflection,
                    'improvement_plan': improvement_plan
                }
            except ImportError:
                # Minimal fallback
                return {
                    'reflection': {
                        "context": "неизвестно",
                        "intent": "неизвестно",
                        "confidence": 0.5,
                        "reasoning": "Minimal fallback reflection",
                        "status": "reflected_with_minimal_fallback",
                        "message": "All reflection components not available"
                    },
                    'improvement_plan': {
                        "areas_for_improvement": ["Integrate all components"],
                        "recommended_actions": ["Install missing dependencies"],
                        "priority": "high",
                        "status": "minimal_improvement_plan"
                    }
                }

    def _handle_improve_command(self, command: AgentCommand) -> Dict[str, Any]:
        """Handle self-improvement commands"""
        payload = command.payload
        reflection_data = payload.get('reflection_data')

        if not reflection_data:
            raise ValueError("No reflection data provided for improvement")

        # Generate improvement plan
        reflection_result = ReflectionOutput(**reflection_data)
        improvement_plan = self._generate_improvement_plan(reflection_result)

        # Execute improvement actions
        improvement_actions = self._execute_improvement_plan(improvement_plan)

        return {
            'improvement_plan': improvement_plan.dict(),
            'actions_executed': improvement_actions
        }

    def _handle_coordinate_command(self, command: AgentCommand) -> Dict[str, Any]:
        """Handle coordination commands"""
        payload = command.payload
        agents = payload.get('agents', [])
        task = payload.get('task')

        if not task:
            raise ValueError("No task provided for coordination")

        # Coordinate agents (simplified for now)
        coordination_result = {
            'task': task,
            'agents_involved': agents,
            'status': 'coordinated',
            'timestamp': datetime.utcnow().isoformat()
        }

        return coordination_result

    def _generate_improvement_plan(self, reflection_result: ReflectionOutput) -> Optional[SelfImprovementPlan]:
        """Generate self-improvement plan based on reflection results"""
        if not self.config.enable_self_improvement:
            return None

        # Analyze reflection results to identify improvement areas
        improvement_areas = []

        # Check for repeated patterns that need improvement
        if reflection_result.is_repeated_pattern:
            improvement_areas.append(f"Handling repeated pattern: {reflection_result.reasoning}")

        # Check for low confidence in context or intent classification
        if "confidence" in reflection_result.reasoning:
            try:
                # Extract confidence values from reasoning
                import re
                context_match = re.search(r'Контекст:.*\((\d+\.\d+)\)', reflection_result.reasoning)
                intent_match = re.search(r'Намерение:.*\((\d+\.\d+)\)', reflection_result.reasoning)

                if context_match and float(context_match.group(1)) < 0.7:
                    improvement_areas.append("Improve context classification accuracy")

                if intent_match and float(intent_match.group(1)) < 0.7:
                    improvement_areas.append("Improve intent identification accuracy")
            except:
                pass

        # Check for negative sentiment that needs handling
        if reflection_result.sentiment and reflection_result.sentiment in ['negative', 'very_negative']:
            improvement_areas.append(f"Improve handling of negative sentiment ({reflection_result.sentiment})")

        if not improvement_areas:
            return None

        # Generate recommended actions
        recommended_actions = []
        for area in improvement_areas:
            if "context classification" in area.lower():
                recommended_actions.append("Train context classifier with more diverse data")
            elif "intent identification" in area.lower():
                recommended_actions.append("Train intent identifier with more specific examples")
            elif "pattern" in area.lower():
                recommended_actions.append("Develop specialized pattern handling strategies")
            elif "sentiment" in area.lower():
                recommended_actions.append("Improve emotion regulation and support strategies")

        # Determine priority
        priority = 'high' if any("pattern" in area.lower() or "sentiment" in area.lower() for area in improvement_areas) else 'medium'

        return SelfImprovementPlan(
            areas_for_improvement=improvement_areas,
            recommended_actions=recommended_actions,
            priority=priority
        )

    def _execute_improvement_plan(self, plan: SelfImprovementPlan) -> List[str]:
        """Execute self-improvement actions"""
        actions_executed = []

        for action in plan.recommended_actions:
            # For now, just log the actions (implementation would depend on specific system)
            logger.info(f"Executing improvement action: {action}")
            actions_executed.append(action)

        return actions_executed

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        return {
            'session_id': self.session_id,
            'metrics': self.performance_metrics,
            'command_history_length': len(self.command_history)
        }

    def get_status(self) -> Dict[str, Any]:
        """Get current status of LLM Core"""
        return {
            'session_id': self.session_id,
            'config': self.config.dict(),
            'components': {
                'memory_enabled': self.config.enable_memory and MEMORY_AVAILABLE,
                'reflection_enabled': self.config.enable_reflection and REFLECTION_AVAILABLE,
                'self_improvement_enabled': self.config.enable_self_improvement,
                'pipeline_coordinator': 'active' if PIPELINE_AVAILABLE else 'unavailable'
            },
            'metrics': self.performance_metrics
        }

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        # Clean up resources if needed
        pass

# Example usage
if __name__ == "__main__":
    # Initialize LLM Core
    core = LLMCore(config=LLMCoreConfig(debug_mode=True))

    # Test processing command
    process_command = AgentCommand(
        command_type='process',
        agent_id='test_agent',
        payload={
            'input_type': 'text',
            'data': 'Это тестовый текст для обработки через LLM Core'
        }
    )

    print("Processing command...")
    response = core.process_command(process_command)
    print(f"Response status: {response.status}")
    print(f"Response result: {json.dumps(response.result, indent=2, ensure_ascii=False) if response.result else 'None'}")

    # Test analysis command
    analyze_command = AgentCommand(
        command_type='analyze',
        agent_id='test_agent',
        payload={
            'text': 'Как улучшить производительность системы?'
        }
    )

    print("\nAnalyzing text...")
    response = core.process_command(analyze_command)
    print(f"Response status: {response.status}")
    print(f"Analysis result: {json.dumps(response.result, indent=2, ensure_ascii=False) if response.result else 'None'}")

    # Get status
    print("\nGetting core status...")
    status = core.get_status()
    print(f"Core status: {json.dumps(status, indent=2, ensure_ascii=False)}")

