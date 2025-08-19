













import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class HeatmapGeneratorAgent:
    """
    Агент для построения интерактивных тепловых карт (например, ценность vs сложность).
    Поддерживает наведение, фильтрацию и динамическое биннинг.
    """

    def run(self, tasks: list, x_field="effort", y_field="value", bin_size=5):
        df = pd.DataFrame(tasks)

        # Validate required fields
        required_fields = {x_field, y_field}
        if not required_fields.issubset(df.columns):
            available = set(df.columns)
            missing = required_fields - available
            raise ValueError(f"Задачи должны содержать поля {missing}. Доступные поля: {available}")

        # Handle missing or invalid data
        df = df.dropna(subset=required_fields)
        if len(df) == 0:
            raise ValueError("Нет действительных данных для построения тепловой карты")

        # Create bins for better visualization
        df["effort_bin"] = pd.cut(df[x_field], bins=bin_size, labels=False)
        df["value_bin"] = pd.cut(df[y_field], bins=bin_size, labels=False)

        # Create heatmap data
        heatmap_data = df.groupby(["value_bin", "effort_bin"]).size().unstack(fill_value=0)

        # Create interactive heatmap
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns if len(heatmap_data.columns) > 0 else [0],
            y=heatmap_data.index if len(heatmap_data.index) > 0 else [0],
            colorscale="YlGnBu",
            hovertemplate="Effort bin: %{x}<br>Value bin: %{y}<br>Count: %{z}<extra></extra>"
        ))

        # Update layout
        fig.update_layout(
            title=f"{y_field.capitalize()} vs {x_field.capitalize()} Heatmap",
            xaxis_title=f"{x_field.capitalize()} (binned)",
            yaxis_title=f"{y_field.capitalize()} (binned)",
            width=600,
            height=450,
            template="plotly_white"
        )

        return fig














