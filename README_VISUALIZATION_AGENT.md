




# Visualization Agent

## Overview

The Visualization Agent is designed to present analysis results and decisions in a clear, visual format. It supports various visualization types including charts, tables, and dashboards, and provides export capabilities to multiple formats.

## Purpose

The Visualization Agent addresses the need to:
- Present priorities, deadlines, task statuses, and category distributions visually
- Support different formats: charts, tables, dashboards
- Enable easy integration with frontend systems
- Provide export capabilities for reporting

## Architecture

The Visualization Agent follows a modular architecture with multiple specialized sub-agents:

### Sub-Agents

1. **DataPreparer** (`data_preparer.py`)
   - Validates, cleans, and aggregates raw data
   - Prepares data for visualization

2. **ChartGenerator** (`chart_generator.py`)
   - Generates various chart types (bar, pie, etc.)
   - Uses a factory pattern for chart creation
   - Provides export to JSON and HTML

3. **TableRenderer** (`table_renderer.py`)
   - Generates HTML tables with customizable headers
   - Exports to CSV and Excel formats

4. **InteractiveController** (`interactive_controller.py`)
   - Manages interactive operations (filtering, sorting)
   - Provides callback mechanism for data updates

5. **ExportManager** (`export_manager.py`)
   - Exports data to various formats (JSON, CSV, Excel)
   - Supports extensibility for additional formats

### Main Agent

**VisualizationAgent** (`visualization_agent.py`)
- Main integration class that coordinates all sub-agents
- Provides comprehensive visualization capabilities
- Handles data preparation, chart generation, table rendering, and exports

## Usage Example

```python
from agents.visualization.visualization_agent import VisualizationAgent

# Create visualization agent
viz_agent = VisualizationAgent()

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
csv_table = table_renderer.export_csv()

# Create interactive controller
def on_update(updated_data):
    print(f"Data updated: {len(updated_data)} items")

interactive_ctrl = viz_agent.create_interactive_controller(tasks, on_update)
interactive_ctrl.filter_by("priority", "high")

# Export data
json_export = viz_agent.export_data(tasks, "json")

# Build dashboard
dashboard = viz_agent.build_dashboard(
    charts=[{"type": "bar", "data": chart_data}],
    tables=[{"data": tasks, "headers": ["id", "title", "priority"]}]
)
```

## Key Features

1. **Data Preparation**: Validates, cleans, and aggregates raw data
2. **Chart Generation**: Supports multiple chart types with customization
3. **Table Rendering**: Generates HTML tables with export capabilities
4. **Interactive Controls**: Filtering, sorting, and real-time updates
5. **Export Capabilities**: JSON, CSV, Excel, and HTML exports
6. **Dashboard Building**: Combines multiple visualizations

## Visualization Types

### Charts
- **Bar Charts**: For comparing categorical data
- **Pie Charts**: For showing proportions
- **Line Charts**: For time series data (extendable)
- **Custom Charts**: Easy to add new chart types

### Tables
- **HTML Tables**: Styled, responsive tables
- **CSV Export**: For Excel and other tools
- **Excel Export**: Direct XLSX generation

### Dashboards
- **Multi-Visualization**: Combine charts and tables
- **Custom Layouts**: Flexible arrangement
- **Exportable**: Full dashboard export

## Integration Capabilities

The Visualization Agent can integrate with:
- Frontend frameworks (React, Vue, Angular)
- Charting libraries (Chart.js, D3.js, Plotly)
- Reporting systems
- Data analysis tools

## Testing

The `test_visualization_agent.py` provides comprehensive test cases demonstrating:
- Data preparation and aggregation
- Chart generation and export
- Table rendering and export
- Interactive data operations
- Dashboard building

## Benefits

1. **Comprehensive Visualization**: Supports all common visualization types
2. **Modular Architecture**: Easy to extend with additional sub-agents
3. **Integration Ready**: Designed for integration with external systems
4. **Export Flexibility**: Multiple export formats for different needs
5. **Interactive Capabilities**: Real-time data manipulation

## Implementation Notes

- The Visualization Agent is designed to work with prepared data
- It's placed in a separate directory for modularity
- The architecture allows for easy extension and customization
- All sub-agents can be independently improved or replaced

## Future Enhancements

- Additional chart types (line, radar, gantt)
- Advanced interactive features (drill-down, tooltips)
- Integration with specific frontend frameworks
- Performance optimization for large datasets
- Template-based dashboard generation

## Dependencies

- Standard Python libraries
- Optional: pandas for Excel export (can be installed with `pip install pandas xlsxwriter`)

## Installation

The Visualization Agent is part of the AI Backlog Assistant package. To use Excel export functionality, install the optional dependencies:

```bash
pip install pandas xlsxwriter
```

## Contributing

To contribute to the Visualization Agent:
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.





