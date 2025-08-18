













import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class HeatmapGeneratorAgent:
    """
    Агент для построения тепловых карт (например, ценность vs сложность).
    """

    def run(self, tasks: list):
        df = pd.DataFrame(tasks)

        if not {"value", "effort"}.issubset(df.columns):
            raise ValueError("Задачи должны содержать поля 'value' и 'effort'")

        fig, ax = plt.subplots()
        heatmap_data = df.pivot_table(index="value", columns="effort", aggfunc="size", fill_value=0)
        sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
        ax.set_title("Value vs Effort Heatmap")
        return fig














