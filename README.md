




# AI BackLog Assistant

## Overview

AI BackLog Assistant is an advanced AI system designed to handle document processing, analysis, and administrative tasks. The system features a modular architecture with LLM Core as the central intelligence module and specialized agents for various tasks.

## Current Status

**Version**: 1.0 (Pre-production)
**Branch**: feature/llm-core-implementation

## Key Components

### 1. LLM Core

The central intelligence module that handles:
- Agent command processing
- Reflection and self-improvement
- Decision making and coordination
- Administrative functions

### 2. ServiceCoordinatorAgent

Dedicated agent for continuous system monitoring and administration:
- Real-time system monitoring
- Alert generation
- Log analysis
- Resource optimization

### 3. Integration Layer

Unified interface that combines LLM Core and ServiceCoordinatorAgent for seamless operation.

## Features

### Core Functionality
- ✅ Document processing pipelines
- ✅ Context analysis and classification
- ✅ Reflection and self-improvement
- ✅ Multi-agent coordination
- ✅ Administrative command handling

### Administrative Features
- ✅ System monitoring
- ✅ Log analysis
- ✅ Resource optimization
- ✅ Alert generation
- ✅ Continuous monitoring

### Testing
- ✅ Unit tests for all components
- ✅ Integration tests
- ✅ Performance monitoring

## Getting Started

### Prerequisites
- Python 3.8+
- Required packages: `pip install -r requirements.txt`

### Installation
```bash
git clone https://github.com/MaksimVF/AI_BackLog_Assistant.git
cd AI_BackLog_Assistant
pip install -r requirements.txt
```

### Running Tests
```bash
# Test LLM Core functionality
python test_llm_core_standalone.py

# Test administrative commands
python test_admin_commands.py

# Test service coordinator
python test_service_coordinator.py

# Test integration
python test_integration.py
```

## Usage

### Basic Usage
```python
from agents.llm_core_standalone import LLMCore, LLMCoreConfig, AgentCommand

# Initialize LLM Core
core = LLMCore(config=LLMCoreConfig(debug_mode=True))

# Process a command
command = AgentCommand(
    command_type='analyze',
    agent_id='user_agent',
    payload={'text': 'Analyze this document'}
)

response = core.process_command(command)
print(response.result)
```

### Administrative Commands
```python
# Monitor system
monitor_command = AgentCommand(
    command_type='monitor_system',
    agent_id='admin_agent',
    payload={}
)

response = core.process_command(monitor_command)
print(response.result['system_status'])

# Analyze logs
log_command = AgentCommand(
    command_type='analyze_logs',
    agent_id='admin_agent',
    payload={'log_data': 'ERROR: Database connection failed'}
)

response = core.process_command(log_command)
print(response.result['log_analysis'])
```

### Service Coordinator
```python
from agents.service_coordinator_agent import ServiceCoordinatorAgent

# Initialize and start monitoring
coordinator = ServiceCoordinatorAgent()
coordinator.start_monitoring(interval=60)

# Get system status
status = coordinator.get_system_status()
print(f"CPU: {status['cpu_usage']}, Memory: {status['memory_usage']}")

# Check alerts
alerts = coordinator.get_alerts()
if alerts:
    print(f"Alerts: {len(alerts)} critical conditions")
```

## Architecture

The system follows a hybrid architecture that combines:
1. **LLM Core** - Central command processing
2. **ServiceCoordinatorAgent** - Continuous monitoring
3. **Specialized Agents** - Task-specific processing

## Documentation

### Current Documentation
- [System Overview](#overview)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [API Reference](docs/API_REFERENCE.md)

### Legacy Documentation
Legacy and outdated documentation has been moved to the `docs/legacy/` directory.

## Development

### Contributing
1. Create a feature branch
2. Implement your changes
3. Add tests
4. Update documentation
5. Create a pull request

### Code Structure
```
.
├── agents/                # Agent implementations
│   ├── llm_core.py        # Main LLM Core
│   ├── llm_core_standalone.py  # Standalone version
│   ├── service_coordinator_agent.py  # Service coordinator
│   └── ...                # Other agents
├── tests/                 # Test scripts
├── docs/                  # Documentation
└── README.md              # This file
```

## Roadmap

### Near-term Goals
- [ ] Integrate real system metrics
- [ ] Add persistent storage for logs
- [ ] Implement web dashboard
- [ ] Enhance security measures

### Long-term Goals
- [ ] Add predictive analytics
- [ ] Implement auto-remediation
- [ ] Add machine learning for optimization
- [ ] Expand agent capabilities

## Support

For issues and feature requests, please use the GitHub issue tracker.

## License

This project is licensed under the MIT License.

---

**Note**: This is a pre-production version. Some features may be subject to change.


