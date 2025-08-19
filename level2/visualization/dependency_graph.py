














import networkx as nx
import plotly.graph_objects as go
import pandas as pd

class DependencyGraphAgent:
    """
    Агент для визуализации интерактивных зависимостей задач в виде графа.
    Поддерживает наведение, перетаскивание узлов и фильтрацию.
    """

    def run(self, tasks: list):
        G = nx.DiGraph()

        # Create graph from tasks
        for task in tasks:
            task_id = str(task.get("id", task.get("title", "unknown")))
            G.add_node(task_id, title=task.get("title", "No title"), **task)
            for dep in task.get("dependencies", []):
                G.add_edge(str(dep), task_id)

        # Prepare data for Plotly
        pos = nx.spring_layout(G)

        # Create edges
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        # Create edge trace
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        # Create node trace
        node_x = []
        node_y = []
        node_text = []
        node_colors = []
        node_sizes = []

        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_data = G.nodes[node]
            title = node_data.get('title', node)
            status = node_data.get('status', 'unknown')
            priority = node_data.get('priority', 'medium')

            # Customize node appearance based on task properties
            if status == 'completed':
                color = 'green'
            elif status == 'in_progress':
                color = 'blue'
            else:
                color = 'lightblue'

            if priority == 'high':
                size = 60
            elif priority == 'low':
                size = 30
            else:
                size = 40

            node_colors.append(color)
            node_sizes.append(size)

            # Create hover text with task details
            hover_text = f"<b>{title}</b><br>"
            hover_text += f"Status: {status}<br>"
            if 'value' in node_data:
                hover_text += f"Value: {node_data['value']}<br>"
            if 'effort' in node_data:
                hover_text += f"Effort: {node_data['effort']}<br>"
            if 'priority' in node_data:
                hover_text += f"Priority: {priority}"

            node_text.append(hover_text)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=[G.nodes[n].get('title', n) for n in G.nodes()],
            textposition="top center",
            hoverinfo='text',
            textfont=dict(size=10),
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                color=node_colors,
                size=node_sizes,
                line_width=2))

        # Add data to traces
        node_trace.text = node_text

        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(
                        title='Task Dependency Graph',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0,l=0,r=0,t=40),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False),
                        template="plotly_white",
                        width=800,
                        height=600
                    ))

        return fig















