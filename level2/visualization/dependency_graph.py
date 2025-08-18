














import networkx as nx
import matplotlib.pyplot as plt

class DependencyGraphAgent:
    """
    Агент для визуализации зависимостей задач в виде графа.
    """

    def run(self, tasks: list):
        G = nx.DiGraph()
        for task in tasks:
            G.add_node(task["id"], label=task["title"])
            for dep in task.get("dependencies", []):
                G.add_edge(dep, task["id"])

        fig, ax = plt.subplots(figsize=(8, 6))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000, ax=ax)
        labels = nx.get_node_attributes(G, "label")
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
        ax.set_title("Dependency Graph")
        return fig















