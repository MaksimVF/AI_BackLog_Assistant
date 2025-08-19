















import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

class TimelineRoadmapAgent:
    """
    Агент для визуализации интерактивной дорожной карты (roadmap) в виде Gantt chart.
    Поддерживает наведение, фильтрацию и отображение дополнительной информации.
    """

    def run(self, tasks: list):
        df = pd.DataFrame(tasks)

        # Validate and prepare date fields
        required_fields = {"start_date", "end_date"}
        if not required_fields.issubset(df.columns):
            available = set(df.columns)
            missing = required_fields - available
            raise ValueError(f"Задачи должны содержать поля {missing}. Доступные поля: {available}")

        # Convert dates and handle missing values
        df["start_date"] = pd.to_datetime(df["start_date"], errors='coerce')
        df["end_date"] = pd.to_datetime(df["end_date"], errors='coerce')
        df = df.dropna(subset=["start_date", "end_date"])

        if len(df) == 0:
            raise ValueError("Нет действительных данных для построения временной шкалы")

        # Add duration and other useful fields
        df["duration_days"] = (df["end_date"] - df["start_date"]).dt.days
        df["status"] = df.apply(lambda x: x.get("status", "planned"), axis=1)

        # Create color mapping based on status
        color_map = {
            "completed": "green",
            "in_progress": "blue",
            "planned": "lightblue",
            "blocked": "red",
            "on_hold": "orange"
        }

        # Create Gantt chart using Plotly
        fig = px.timeline(
            df,
            x_start="start_date",
            x_end="end_date",
            y="title",
            color="status",
            color_discrete_map=color_map,
            title="Project Roadmap Timeline",
            hover_data={
                "start_date": "|%B %d, %Y",
                "end_date": "|%B %d, %Y",
                "duration_days": True,
                "status": True
            }
        )

        # Customize hover template
        fig.update_traces(
            hovertemplate="<b>%{y}</b><br>" +
                         "Start: %{customdata[0]}<br>" +
                         "End: %{customdata[1]}<br>" +
                         "Duration: %{customdata[2]} days<br>" +
                         "Status: %{customdata[3]}<extra></extra>"
        )

        # Update layout
        fig.update_layout(
            width=800,
            height=500,
            template="plotly_white",
            xaxis_title="Time",
            yaxis_title="Tasks",
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Rockwell"
            )
        )

        # Add milestones if available
        if "milestone" in df.columns:
            milestones = df[df["milestone"] == True]
            for i, row in milestones.iterrows():
                fig.add_vline(
                    x=row["start_date"],
                    line_dash="dash",
                    line_color="red",
                    annotation_text=row["title"],
                    annotation_position="top left"
                )

        return fig
















