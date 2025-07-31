

# Decision Agent Implementation

## Overview

This implementation provides a comprehensive Decision Agent system that integrates with the existing prioritization framework to make informed decisions about task execution. The system follows a modular architecture with three main components:

1. **FactorAnalyzer** - Analyzes task factors (priority, effort, criticality, risk)
2. **DecisionLogic** - Applies business rules to make decisions (recommend, postpone, reject)
3. **RecommendationReporter** - Generates structured reports with explanations

## Architecture

The Decision Agent integrates with the existing prioritization system to provide a complete solution for task decision making.

### Components

1. **FactorAnalyzer** (`factor_analyzer.py`)
   - Analyzes task factors including priority, effort, criticality, and risk
   - Returns structured factor analysis for decision making

2. **DecisionLogic** (`decision_logic.py`)
   - Applies configurable business rules to make decisions
   - Uses weighted scoring based on priority, criticality, and effort
   - Returns one of three decisions: recommend, postpone, or reject

3. **RecommendationReporter** (`recommendation_reporter.py`)
   - Generates structured reports with decision explanations
   - Provides detailed reasoning for each decision

4. **DecisionAgent** (`decision_agent_integration.py`)
   - Main integration class that combines all components
   - Integrates with existing PrioritizationAgent for comprehensive analysis
   - Provides both individual and batch decision making

## Usage Example

```python
from agents.prioritization.decision_agent_integration import DecisionAgent
from agents.prioritization.models import TaskData

# Create decision agent
agent = DecisionAgent()

# Sample task
task = TaskData(
    task_id="task_1",
    title="Critical security fix",
    description="Fix critical vulnerability in authentication system",
    impact=9,
    urgency=8,
    is_blocking=True,
    effort=2
)

# Make decision
result = agent.make_decision(task)

print(f"Decision: {result['decision']}")
print(f"Report: {result['report']}")
print(f"Priority Analysis: {result['priority_analysis']}")
```

## Decision Making Process

1. **Prioritization**: Task is analyzed by the PrioritizationAgent to determine score, criticality, and other metrics
2. **Factor Analysis**: Additional factors are analyzed and combined with prioritization results
3. **Decision Logic**: Business rules are applied to determine the final decision
4. **Report Generation**: Structured report is generated with explanations and details

## Configuration

The decision thresholds can be adjusted in the `DecisionLogic` class:
- Recommendation threshold: score > 100 and criticality >= 7
- Postpone threshold: score > 50 or criticality >= 5
- Reject: anything below postpone threshold

## Testing

The `test_decision_agent.py` provides example usage and demonstrates the decision making process with sample tasks.

## Integration

The Decision Agent is designed to work seamlessly with the existing prioritization system, leveraging all the existing analysis capabilities while adding the final decision-making layer.

