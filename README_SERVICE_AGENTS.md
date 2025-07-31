






# Service Agents

## Overview

The Service Agents provide essential support functions for the AI Backlog Assistant, including auditing, feedback collection, and fallback planning. These agents ensure transparency, continuous improvement, and system resilience.

## Purpose

The Service Agents address the need to:
- Track decision-making processes and results
- Collect user feedback for system improvement
- Provide fallback strategies when agents fail
- Maintain system transparency and accountability

## Architecture

The Service Agents follow a modular architecture with specialized agents:

### Agents

1. **AuditAgent** (`audit_agent.py`)
   - Records decision-making trace, parameters, results, status, and timestamps
   - Provides transparency and accountability

2. **FeedbackAgent** (`feedback_agent.py`)
   - Collects and stores user feedback on results
   - Enables continuous system improvement

3. **FallbackPlanner** (`fallback_planner.py`)
   - Provides fallback strategies when agents fail or timeout
   - Ensures system resilience and reliability

### Storage

**InMemoryStorage** (`mock_storage.py`)
- Mock storage implementation for testing
- Can be replaced with database, file, or API storage

## Usage Example

```python
from agents.service.audit_agent import AuditAgent
from agents.service.feedback_agent import FeedbackAgent
from agents.service.fallback_planner import FallbackPlanner
from agents.service.mock_storage import InMemoryStorage

# Initialize storage
storage = InMemoryStorage()

# Initialize agents
audit_agent = AuditAgent(storage)
feedback_agent = FeedbackAgent(storage)

# Fallback configuration
fallback_config = {
    "ChartGenerator": {
        "TimeoutError": "TableRenderer",
        "ValueError": "SimplifiedChartMode"
    }
}
fallback_planner = FallbackPlanner(fallback_config)

# Record audit information
audit_record = audit_agent.run(
    task_id="T123",
    inputs={"param1": "value1"},
    outputs={"result": "ok"},
    agent_chain=["InputCollector", "ScorerAgent"],
    user_id="U456"
)

# Collect user feedback
feedback_record = feedback_agent.run(
    task_id="T123",
    user_rating="positive",
    user_comment="Great results!",
    user_id="U456"
)

# Get fallback strategy
fallback_strategy = fallback_planner.run({
    "agent": "ChartGenerator",
    "error_type": "TimeoutError",
    "attempt": 1
})
```

## Audit Agent

### Purpose
Records decision-making trace, parameters, results, status, and timestamps.

### Inputs
- `task_id`: Task identifier
- `inputs`: Input parameters
- `outputs`: Output results
- `agent_chain`: List of agents in pipeline
- `user_id`: User identifier (optional)

### Outputs
- `audit_record`: Dictionary containing audit information

### Storage
Requires a storage backend with `save_audit(record)` method.

## Feedback Agent

### Purpose
Collects and stores user feedback on results.

### Inputs
- `task_id`: Task identifier
- `user_rating`: User rating ('positive', 'negative', 'neutral')
- `user_comment`: User comment (optional)
- `user_id`: User identifier (optional)

### Outputs
- `feedback_record`: Dictionary containing feedback information

### Storage
Requires a storage backend with `save_feedback(record)` method.

## Fallback Planner

### Purpose
Provides fallback strategies when agents fail or timeout.

### Inputs
- `error_context`: Dictionary containing error information
  - `agent`: Agent name
  - `error_type`: Error type
  - `attempt`: Attempt number

### Outputs
- `fallback_strategy`: Dictionary containing fallback strategy

### Configuration
Accepts a fallback configuration dictionary:
```python
fallback_config = {
    "ChartGenerator": {
        "TimeoutError": "TableRenderer",
        "ValueError": "SimplifiedChartMode"
    },
    "SchedulingIntegrator": {
        "APIError": "ManualExport"
    }
}
```

## Testing

The service agents include comprehensive test cases:

### Test Files
- `test_audit_agent.py`: Tests audit recording functionality
- `test_feedback_agent.py`: Tests feedback collection functionality
- `test_fallback_planner.py`: Tests fallback strategy determination

### Test Cases
- Audit agent saves records correctly
- Audit agent handles missing user_id
- Feedback agent saves feedback correctly
- Feedback agent handles missing comment
- Feedback agent handles missing user_id
- Fallback planner returns configured fallback
- Fallback planner handles unknown cases
- Fallback planner works without configuration

## Key Features

1. **Transparency**: Audit trail for all decisions
2. **Improvement**: User feedback collection
3. **Resilience**: Fallback strategies for failures
4. **Modularity**: Separate agents for different functions
5. **Extensibility**: Easy to add new storage backends
6. **Testability**: Comprehensive test coverage

## Benefits

1. **Accountability**: Clear record of all decisions
2. **Continuous Improvement**: User feedback drives enhancements
3. **Reliability**: System continues to function despite failures
4. **Flexibility**: Works with different storage backends
5. **Maintainability**: Clear separation of concerns

## Implementation Notes

- The service agents are designed to work with any storage backend
- They're placed in a separate directory for modularity
- The architecture allows for easy extension and customization
- All agents can be independently improved or replaced

## Future Enhancements

- Database storage integration
- Advanced audit analysis
- Feedback analytics
- Machine learning for fallback strategy optimization
- Integration with monitoring systems

## Dependencies

- Standard Python libraries
- No external dependencies required

## Installation

The Service Agents are part of the AI Backlog Assistant package and require no additional installation.

## Contributing

To contribute to the Service Agents:
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.







