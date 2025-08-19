















import plotly.io as pio
from .interactive_dashboard import InteractiveDashboardAgent
from .heatmap_generator import HeatmapGeneratorAgent
from .dependency_graph import DependencyGraphAgent
from .timeline_roadmap import TimelineRoadmapAgent

class VisualizationAggregator:
    """
    Агрегатор модулей визуализации (второй уровень).
    Поддерживает как интерактивные Plotly визуализации, так и статические экспорты.
    """

    def __init__(self):
        self.dashboard = InteractiveDashboardAgent()
        self.heatmap = HeatmapGeneratorAgent()
        self.graph = DependencyGraphAgent()
        self.timeline = TimelineRoadmapAgent()

    def run(self, tasks: list, output_format="plotly") -> dict:
        """
        Запускает визуализации.

        Args:
            tasks: Список задач для визуализации
            output_format: Формат вывода ('plotly' для интерактивных, 'static' для изображений)

        Returns:
            Словарь с результатами визуализаций
        """
        results = {}

        # Generate all visualizations
        try:
            results["dashboard"] = self.dashboard.run(tasks)
        except Exception as e:
            results["dashboard_error"] = str(e)

        try:
            results["heatmap"] = self.heatmap.run(tasks)
        except Exception as e:
            results["heatmap_error"] = str(e)

        try:
            results["dependency_graph"] = self.graph.run(tasks)
        except Exception as e:
            results["dependency_graph_error"] = str(e)

        try:
            results["timeline"] = self.timeline.run(tasks)
        except Exception as e:
            results["timeline_error"] = str(e)

        # Convert to requested format
        if output_format == "static":
            results = self._convert_to_static(results)

        return results

    def _convert_to_static(self, plotly_figures: dict) -> dict:
        """
        Конвертирует Plotly фигуры в статические изображения (PNG).
        """
        static_results = {}

        for key, fig in plotly_figures.items():
            if key.endswith("_error"):
                static_results[key] = fig
                continue

            try:
                # Convert Plotly figure to PNG
                static_img = pio.to_image(fig, format="png")
                static_results[key] = static_img
            except Exception as e:
                static_results[f"{key}_error"] = str(e)

        return static_results

    def to_html(self, plotly_figures: dict) -> str:
        """
        Конвертирует все визуализации в HTML для встраивания в веб-страницы.
        """
        html_parts = []

        for key, fig in plotly_figures.items():
            if key.endswith("_error"):
                html_parts.append(f"<h3>{key}</h3><p>Error: {fig}</p>")
                continue

            try:
                html_parts.append(f"<h3>{key.capitalize().replace('_', ' ')}</h3>")
                html_parts.append(pio.to_html(fig, full_html=False))
            except Exception as e:
                html_parts.append(f"<h3>{key}</h3><p>Error generating HTML: {str(e)}</p>")

        return "\n".join(html_parts)

















