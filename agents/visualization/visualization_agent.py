





"""
Visualization Agent

Main agent that integrates all visualization sub-agents.
"""

from typing import Dict, Any, List, Optional
from .data_preparer import DataPreparer
from .chart_generator import ChartFactory, ChartExporter
from .table_renderer import TableRenderer
from .interactive_controller import InteractiveController
from .export_manager import ExportManager

class VisualizationAgent:
    """
    Main visualization agent that integrates all sub-agents.
    """

    def __init__(self):
        """Initialize with all sub-agents"""
        self.data_preparer = None
        self.chart_factory = ChartFactory()
        self.chart_exporter = None
        self.table_renderer = None
        self.interactive_controller = None
        self.export_manager = None

    def prepare_data(self, raw_data: List[Dict[str, Any]]) -> DataPreparer:
        """
        Prepares data for visualization.

        Args:
            raw_data: Raw data to prepare

        Returns:
            DataPreparer instance
        """
        self.data_preparer = DataPreparer(raw_data)
        self.data_preparer.validate()
        self.data_preparer.clean()
        return self.data_preparer

    def generate_chart(self, chart_type: str, data: Dict[str, Any], options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generates chart visualization.

        Args:
            chart_type: Type of chart ('bar', 'pie', etc.)
            data: Chart data
            options: Chart options

        Returns:
            Chart configuration
        """
        if options is None:
            options = {}

        renderer = self.chart_factory.create_renderer(chart_type, data, options)
        chart_data = renderer.render()
        self.chart_exporter = ChartExporter(chart_data)
        return chart_data

    def export_chart(self, format: str = "html") -> str:
        """
        Exports chart to specified format.

        Args:
            format: Export format ('html', 'json')

        Returns:
            Exported chart data
        """
        if not self.chart_exporter:
            raise ValueError("No chart has been generated yet")

        if format == "html":
            return self.chart_exporter.export_as_html()
        elif format == "json":
            return self.chart_exporter.export_as_json()
        else:
            raise ValueError(f"Unsupported chart export format: {format}")

    def render_table(self, data: List[Dict[str, Any]], headers: Optional[List[str]] = None) -> TableRenderer:
        """
        Renders data as table.

        Args:
            data: Table data
            headers: Column headers

        Returns:
            TableRenderer instance
        """
        self.table_renderer = TableRenderer(data, headers)
        return self.table_renderer

    def export_table(self, format: str = "html") -> str:
        """
        Exports table to specified format.

        Args:
            format: Export format ('html', 'csv', 'excel')

        Returns:
            Exported table data
        """
        if not self.table_renderer:
            raise ValueError("No table has been rendered yet")

        if format == "html":
            return self.table_renderer.render_html()
        elif format == "csv":
            return self.table_renderer.export_csv()
        elif format == "excel":
            return self.table_renderer.export_excel()
        else:
            raise ValueError(f"Unsupported table export format: {format}")

    def create_interactive_controller(self, data: List[Dict[str, Any]], on_update: Optional[callable] = None) -> InteractiveController:
        """
        Creates interactive data controller.

        Args:
            data: Interactive data
            on_update: Update callback

        Returns:
            InteractiveController instance
        """
        self.interactive_controller = InteractiveController(data, on_update)
        return self.interactive_controller

    def export_data(self, data: List[Dict[str, Any]], format: str = "json") -> bytes:
        """
        Exports data to specified format.

        Args:
            data: Data to export
            format: Export format ('json', 'csv', 'excel')

        Returns:
            Exported data as bytes
        """
        self.export_manager = ExportManager(data)
        return self.export_manager.export(format)

    def build_dashboard(self, charts: List[Dict[str, Any]], tables: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Builds a dashboard with multiple visualizations.

        Args:
            charts: List of chart configurations
            tables: List of table configurations

        Returns:
            Dashboard configuration
        """
        dashboard = {
            "charts": [],
            "tables": []
        }

        for chart_config in charts:
            chart_type = chart_config.get("type", "bar")
            chart_data = chart_config.get("data", {})
            chart_options = chart_config.get("options", {})
            chart = self.generate_chart(chart_type, chart_data, chart_options)
            dashboard["charts"].append(chart)

        for table_config in tables:
            table_data = table_config.get("data", [])
            table_headers = table_config.get("headers", [])
            table = self.render_table(table_data, table_headers)
            dashboard["tables"].append({
                "headers": table_headers,
                "html": table.render_html()
            })

        return dashboard







