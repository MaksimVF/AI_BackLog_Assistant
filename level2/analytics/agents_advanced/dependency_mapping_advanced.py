









import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, Any, Tuple, Optional
from level2.dto import Task
from ..dto_advanced import DependencyConfigAdvanced
from ..utils import safe_float
import os

class DependencyMappingAdvancedAgent:
    name = "DEPENDENCY_MAPPING_ADV"

    def _build_graph(self, task: Task, repo_fetcher, max_depth: int) -> nx.DiGraph:
        G = nx.DiGraph()
        # Построение графа зависимостей
        nodes = set()
        edges = set()

        # Начинаем с текущей задачи
        frontier = [(task.id, 0)]
        while frontier:
            current_id, depth = frontier.pop(0)
            if current_id in nodes or depth > max_depth:
                continue
            nodes.add(current_id)

            # Получаем задачу
            current_task = repo_fetcher(current_id) if repo_fetcher else None
            if not current_task:
                continue

            # Добавляем зависимости
            for dep_id in current_task.dependencies or []:
                if dep_id not in nodes:
                    edges.add((current_id, dep_id))
                    frontier.append((dep_id, depth + 1))

        # Добавляем узлы и рёбра в граф
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        return G

    def score(self, task: Task, cfg: DependencyConfigAdvanced, repo_fetcher) -> Tuple[float, Dict[str, Any], Dict[str, str]]:
        G = self._build_graph(task, repo_fetcher, cfg.max_depth)

        # Анализ графа
        cycles = list(nx.simple_cycles(G))
        critical_path = nx.dag_longest_path(G) if nx.is_directed_acyclic_graph(G) else []

        details = {
            "nodes": len(G.nodes),
            "edges": len(G.edges),
            "cycles": cycles,
            "critical_path": critical_path
        }

        # Визуализация
        if cfg.visualize:
            plt.figure(figsize=(10, 6))
            nx.draw(G, with_labels=True)
            output_path = os.path.join(cfg.output_dir or "/tmp", f"dependency_graph_{task.id}.png")
            plt.savefig(output_path)
            details["visualization_path"] = output_path

        # Оценка сложности
        complexity = len(G.nodes) / 10.0  # Пример оценки

        return complexity, details, {"DEPENDENCY": "COMPLEX" if complexity > 0.5 else "SIMPLE"}









