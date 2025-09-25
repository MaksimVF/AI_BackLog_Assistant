

# Level 4 Visualization Agents

## Overview

Level 4 contains advanced visualization agents that provide comprehensive data presentation capabilities using LangGraph patterns. These agents are designed to work with data from previous levels and provide enhanced visual insights.

## Architecture

The Level 4 visualization architecture follows a modular design with LangGraph-enhanced agents:

### Directory Structure

```
src/v2/agents/level4/
├── __init__.py
├── visualization/
│   ├── __init__.py
│   ├── langgraph_data_preparer.py
│   ├── langgraph_chart_generator.py
│   ├── langgraph_table_renderer.py
│   ├── langgraph_interactive_controller.py
│   ├── langgraph_export_manager.py
│   └── langgraph_visualization_agent.py
```

### Key Components

1. **LangGraphDataPreparer** - Enhanced data validation, cleaning, and aggregation
2. **LangGraphChartGenerator** - Advanced chart generation with contextual understanding
3. **LangGraphTableRenderer** - Table rendering with relationship detection
4. **LangGraphInteractiveController** - Interactive data operations with contextual awareness
5. **LangGraphExportManager** - Data export with contextual information preservation
6. **LangGraphVisualizationAgent** - Main coordinator for all visualization agents

## Features

### Enhanced Capabilities

- **Contextual Understanding**: All agents use LangGraph patterns to detect relationships
- **Relationship Detection**: Automatic pattern and relationship identification
- **Contextual Export**: Preserves contextual information during export
- **Interactive Insights**: Enhanced interactive operations with contextual feedback
- **Quality Analysis**: Built-in visualization quality assessment

### Backward Compatibility

- Maintains the same interface as version 1.0 visualization agents
- Can work with existing data structures
- Provides enhanced functionality while preserving core features

## Usage

### Basic Usage

```python
from src.v2.agents.level4.visualization.langgraph_visualization_agent import LangGraphVisualizationAgent

# Create visualization agent
viz_agent = LangGraphVisualizationAgent()

# Sample data
tasks = [
    {"id": 1, "title": "Fix security vulnerability", "priority": "high", "category": "security"},
    {"id": 2, "title": "Update UI components", "priority": "medium", "category": "ui"},
    {"id": 3, "title": "Add documentation", "priority": "low", "category": "docs"},
]

# Prepare data
data_preparer = viz_agent.prepare_data(tasks)
aggregated = data_preparer.aggregate(["priority"])

# Generate chart
chart_data = {
    "title": "Tasks by Priority",
    "x_axis": ["high", "medium", "low"],
    "y_axis": [1, 1, 1]
}
chart_config = viz_agent.generate_chart("bar", chart_data)
html_chart = viz_agent.export_chart("html")

# Render table
table_renderer = viz_agent.render_table(tasks, ["id", "title", "priority"])
html_table = table_renderer.render_html()
```

### Pipeline Usage

```python
from src.v2.pipelines.level4_pipeline import Level4Pipeline

# Create pipeline
pipeline = Level4Pipeline()

# Process visualization
result = pipeline.process_visualization(
    data=tasks,
    visualization_config={
        "charts": [{"type": "bar", "data": chart_data}],
        "tables": [{"data": tasks, "headers": ["id", "title", "priority"]}],
        "interactive": True
    }
)

# Generate dashboard
dashboard = pipeline.generate_dashboard(tasks, dashboard_config)
```

## Integration

### With Level 2

The Level 4 visualization agents can work with data processed by Level 2 agents. The pipeline accepts data from Level 2 and enhances it with visualization capabilities.

### With Existing Systems

The agents maintain backward compatibility with version 1.0 interfaces, allowing for gradual migration and integration with existing systems.

## Testing

Comprehensive test cases are available in `test_level4_visualization.py` that demonstrate:

- Data preparation and aggregation
- Chart generation and export
- Table rendering and export
- Interactive data operations
- Dashboard building
- Quality analysis

## Benefits

1. **Enhanced Visualization**: Advanced contextual understanding improves visualization quality
2. **Relationship Detection**: Automatic pattern detection provides deeper insights
3. **Context Preservation**: Maintains contextual information throughout the visualization process
4. **Modular Architecture**: Easy to extend and customize individual components
5. **Backward Compatibility**: Works with existing data structures and interfaces

## Future Enhancements

- Additional chart types with LangGraph enhancements
- Advanced interactive features with contextual feedback
- Integration with specific frontend frameworks
- Performance optimization for large datasets
- Template-based dashboard generation

## Dependencies

- Standard Python libraries
- CrewAI for LangGraph capabilities
- Optional: pandas for Excel export (can be installed with `pip install pandas xlsxwriter`)

## Implementation Notes

- The Level 4 agents are designed to work with data from previous levels
- All agents use LangGraph patterns for enhanced contextual understanding
- The architecture allows for easy extension and customization
- All sub-agents can be independently improved or replaced

