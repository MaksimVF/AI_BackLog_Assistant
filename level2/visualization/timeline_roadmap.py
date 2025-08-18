















import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

class TimelineRoadmapAgent:
    """
    Агент для визуализации дорожной карты (roadmap) в виде Gantt chart.
    """

    def run(self, tasks: list):
        df = pd.DataFrame(tasks)

        if not {"start_date", "end_date"}.issubset(df.columns):
            raise ValueError("Задачи должны содержать 'start_date' и 'end_date'")

        df["start_date"] = pd.to_datetime(df["start_date"])
        df["end_date"] = pd.to_datetime(df["end_date"])

        fig, ax = plt.subplots(figsize=(10, 6))
        for i, row in df.iterrows():
            ax.barh(row["title"], (row["end_date"] - row["start_date"]).days,
                    left=row["start_date"], color="skyblue")

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.xticks(rotation=45)
        ax.set_title("Project Roadmap Timeline")
        return fig
















