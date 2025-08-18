















from .interactive_dashboard import InteractiveDashboardAgent
from .heatmap_generator import HeatmapGeneratorAgent
from .dependency_graph import DependencyGraphAgent
from .timeline_roadmap import TimelineRoadmapAgent

class VisualizationAggregator:
    """
    Агрегатор модулей визуализации (второй уровень).
    """

    def __init__(self):
        self.dashboard = InteractiveDashboardAgent()
        self.heatmap = HeatmapGeneratorAgent()
        self.graph = DependencyGraphAgent()
        self.timeline = TimelineRoadmapAgent()

    async def run(self, tasks: list) -> dict:
        """
        Запускает визуализации. Возвращает фигуры matplotlib.
        """
        results = {}
        results["dashboard"] = self.dashboard.run(tasks)
        results["heatmap"] = self.heatmap.run(tasks)
        results["dependency_graph"] = self.graph.run(tasks)
        results["timeline"] = self.timeline.run(tasks)
        return results

















