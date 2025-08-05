




# AI BackLog Assistant - API Reference

## Table of Contents

1. [LLM Core API](#llm-core-api)
2. [ServiceCoordinatorAgent API](#servicecoordinatoragent-api)
3. [AgentCommand Structure](#agentcommand-structure)
4. [AgentResponse Structure](#agentresponse-structure)
5. [Error Handling](#error-handling)

## LLM Core API

### Initialization

```python
from agents.llm_core_standalone import LLMCore, LLMCoreConfig

# Initialize LLM Core
config = LLMCoreConfig(
    debug_mode=True,
    max_retries=3,
    timeout=30
)
core = LLMCore(config=config)
```

### Process Command

```python
from agents.llm_core_standalone import AgentCommand

command = AgentCommand(
    command_type='analyze',
    agent_id='user_agent',
    payload={'text': 'Analyze this document'}
)

response = core.process_command(command)
```

### Administrative Commands

#### Monitor System

```python
command = AgentCommand(
    command_type='monitor_system',
    agent_id='admin_agent',
    payload={}
)

response = core.process_command(command)
# Returns system status in response.result['system_status']
```

#### Analyze Logs

```python
command = AgentCommand(
    command_type='analyze_logs',
    agent_id='admin_agent',
    payload={'log_data': 'ERROR: Database connection failed'}
)

response = core.process_command(command)
# Returns log analysis in response.result['log_analysis']
```

#### Optimize Resources

```python
command = AgentCommand(
    command_type='optimize_resources',
    agent_id='admin_agent',
    payload={'system_status': current_status}
)

response = core.process_command(command)
# Returns recommendations in response.result['optimization_recommendations']
```

### Status and Metrics

```python
status = core.get_status()
# Returns current status and metrics
```

## ServiceCoordinatorAgent API

### Initialization

```python
from agents.service_coordinator_agent import ServiceCoordinatorAgent

coordinator = ServiceCoordinatorAgent(config={
    'monitoring_interval': 60,
    'alert_thresholds': {
        'cpu': 90,
        'memory': 85,
        'disk': 20
    }
})
```

### Monitoring

```python
# Start continuous monitoring
coordinator.start_monitoring(interval=60)

# Stop monitoring
coordinator.stop_monitoring()
```

### System Status

```python
status = coordinator.get_system_status()
# Returns current system status
```

### Alerts

```python
alerts = coordinator.get_alerts()
# Returns list of active alerts
```

### Log Analysis

```python
analysis = coordinator.analyze_logs(log_data)
# Returns log analysis results
```

### Optimization

```python
recommendations = coordinator.get_optimization_recommendations()
# Returns resource optimization recommendations
```

## AgentCommand Structure

```python
from agents.llm_core_standalone import AgentCommand

command = AgentCommand(
    command_type='analyze',  # One of: process, analyze, route, reflect, improve, coordinate, monitor_system, analyze_logs, optimize_resources
    agent_id='user_agent',   # ID of the requesting agent
    payload={                # Command-specific data
        'text': 'Document content to analyze',
        'context': {...}
    },
    metadata={               # Optional metadata
        'timestamp': '2025-08-05T12:00:00Z',
        'priority': 'high'
    }
)
```

## AgentResponse Structure

```python
response = {
    'status': 'success',     # One of: success, error, pending
    'command_id': 'cmd_123', # Unique command identifier
    'result': {              # Command-specific result
        'analysis': {...},
        'system_status': {...},
        'log_analysis': {...},
        'optimization_recommendations': [...]
    },
    'metrics': {             # Performance metrics
        'processing_time': 0.45,
        'tokens_used': 1200
    },
    'error': None            # Error information (if any)
}
```

## Error Handling

### Common Errors

- **InvalidCommandError**: Invalid command type or structure
- **ProcessingError**: Error during command processing
- **TimeoutError**: Command processing timed out
- **ResourceError**: Insufficient resources to process command

### Error Response

```python
response = {
    'status': 'error',
    'command_id': 'cmd_123',
    'result': None,
    'metrics': {},
    'error': {
        'type': 'InvalidCommandError',
        'message': 'Invalid command type: unknown_command',
        'details': 'Command type must be one of: process, analyze, route, reflect, improve, coordinate, monitor_system, analyze_logs, optimize_resources'
    }
}
```

## Integration Example

```python
from agents.llm_core_standalone import LLMCore, LLMCoreConfig, AgentCommand
from agents.service_coordinator_agent import ServiceCoordinatorAgent

# Initialize components
core = LLMCore(config=LLMCoreConfig(debug_mode=True))
coordinator = ServiceCoordinatorAgent()

# Start monitoring
coordinator.start_monitoring(interval=60)

# Get system status
status = coordinator.get_system_status()

# Send to LLM Core for optimization
command = AgentCommand(
    command_type='optimize_resources',
    agent_id='admin_agent',
    payload={'system_status': status}
)

response = core.process_command(command)
recommendations = response.result['optimization_recommendations']

print("Optimization Recommendations:")
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec}")

# Check for alerts
alerts = coordinator.get_alerts()
if alerts:
    print(f"Critical Alerts: {len(alerts)}")
    for alert in alerts:
        print(f"- {alert['message']}")
```

## Best Practices

1. **Use Contextual Commands**: Always include relevant context in command payloads
2. **Handle Errors Gracefully**: Implement proper error handling for all commands
3. **Monitor Performance**: Use metrics to track system performance
4. **Regular Maintenance**: Periodically check system status and alerts
5. **Secure Communications**: Use authentication for administrative commands

## Versioning

The API follows semantic versioning:
- **Major**: Breaking changes
- **Minor**: New features (backward compatible)
- **Patch**: Bug fixes and improvements

Current version: 1.0.0 (Pre-production)


