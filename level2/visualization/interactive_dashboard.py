












import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class InteractiveDashboardAgent:
    """
    Агент для построения интерактивного дашборда с использованием Plotly.
    Поддерживает фильтрацию, наведение и другие интерактивные функции.
    """

    def run(self, tasks: list):
        df = pd.DataFrame(tasks)

        # Create summary statistics
        status_summary = df.groupby("status").size().reset_index(name="count")
        priority_summary = df.groupby("priority").size().reset_index(name="count") if "priority" in df else None

        # Create interactive figure
        fig = make_subplots(
            rows=1, cols=2 if priority_summary is not None else 1,
            subplot_titles=("Tasks by Status", "Tasks by Priority") if priority_summary is not None else ("Tasks by Status",)
        )

        # Add status bar chart
        bar_status = go.Bar(
            x=status_summary["status"],
            y=status_summary["count"],
            name="Status",
            marker_color="rgb(55, 83, 109)"
        )
        fig.add_trace(bar_status, row=1, col=1)

        # Add priority bar chart if available
        if priority_summary is not None:
            bar_priority = go.Bar(
                x=priority_summary["priority"],
                y=priority_summary["count"],
                name="Priority",
                marker_color="rgb(26, 118, 255)"
            )
            fig.add_trace(bar_priority, row=1, col=2)

        # Update layout
        fig.update_layout(
            height=400,
            width=800 if priority_summary is not None else 400,
            title_text="Project Dashboard",
            showlegend=True,
            hovermode="closest",
            template="plotly_white"
        )

        # Add interactive features
        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>"
        )

        return fig













