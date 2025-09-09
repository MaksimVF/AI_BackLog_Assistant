




"""
Chart Generator Agent

Generates various types of charts from prepared data.
"""

import json
from typing import Dict, Any, List

class ChartRenderer:
    """
    Base class for chart renderers.
    """

    def __init__(self, data: Dict[str, Any], options: Dict[str, Any]):
        self.data = data
        self.options = options

    def render(self) -> Dict[str, Any]:
        """
        Renders chart configuration.
        """
        raise NotImplementedError("Render method not implemented")

class BarChartRenderer(ChartRenderer):
    """
    Renders bar charts.
    """

    def render(self) -> Dict[str, Any]:
        """
        Generates bar chart configuration.
        """
        return {
            "type": "bar",
            "data": {
                "labels": self.data["x_axis"],
                "datasets": [{
                    "label": self.data.get("title", "Data"),
                    "data": self.data["y_axis"],
                    "backgroundColor": self._generate_colors()
                }]
            },
            "options": self._build_options()
        }

    def _generate_colors(self) -> List[str]:
        """
        Generates color scheme.
        """
        scheme = self.options.get("color_scheme", "default")
        if scheme == "pastel":
            return ["#A8DADC", "#457B9D", "#1D3557", "#E63946", "#F1FAEE"]
        return ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"]

    def _build_options(self) -> Dict[str, Any]:
        """
        Builds chart options.
        """
        return {
            "responsive": self.options.get("responsive", True),
            "plugins": {
                "legend": {
                    "position": self.options.get("legend_position", "top")
                },
                "title": {
                    "display": True,
                    "text": self.data.get("title", ""),
                    "font": {"size": self.options.get("title_font_size", 16)}
                }
            }
        }

class PieChartRenderer(ChartRenderer):
    """
    Renders pie charts.
    """

    def render(self) -> Dict[str, Any]:
        """
        Generates pie chart configuration.
        """
        return {
            "type": "pie",
            "data": {
                "labels": self.data["x_axis"],
                "datasets": [{
                    "data": self.data["y_axis"],
                    "backgroundColor": self._generate_colors()
                }]
            },
            "options": self._build_options()
        }

    def _generate_colors(self) -> List[str]:
        """
        Generates color scheme.
        """
        return ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"]

    def _build_options(self) -> Dict[str, Any]:
        """
        Builds chart options.
        """
        return {
            "responsive": self.options.get("responsive", True),
            "plugins": {
                "legend": {
                    "position": self.options.get("legend_position", "bottom")
                },
                "title": {
                    "display": True,
                    "text": self.data.get("title", ""),
                    "font": {"size": self.options.get("title_font_size", 16)}
                }
            }
        }

class ChartFactory:
    """
    Factory for creating chart renderers.
    """

    @staticmethod
    def create_renderer(chart_type: str, data: Dict[str, Any], options: Dict[str, Any]) -> ChartRenderer:
        """
        Creates appropriate chart renderer.

        Args:
            chart_type: Type of chart ('bar', 'pie', etc.)
            data: Chart data
            options: Chart options

        Returns:
            ChartRenderer instance
        """
        if chart_type == "bar":
            return BarChartRenderer(data, options)
        elif chart_type == "pie":
            return PieChartRenderer(data, options)
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")

class ChartExporter:
    """
    Exports chart configurations to various formats.
    """

    def __init__(self, chart_data: Dict[str, Any]):
        self.chart_data = chart_data

    def export_as_json(self) -> str:
        """
        Exports chart as JSON.
        """
        return json.dumps(self.chart_data, indent=2, ensure_ascii=False)

    def export_as_html(self) -> str:
        """
        Exports chart as HTML with Chart.js integration.
        """
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <canvas id="chartCanvas" style="max-width: 800px; max-height: 400px;"></canvas>
            <script>
                const ctx = document.getElementById('chartCanvas');
                const config = {json.dumps(self.chart_data)};
                new Chart(ctx, config);
            </script>
        </body>
        </html>
        """





