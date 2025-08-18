












import matplotlib.pyplot as plt
import pandas as pd

class InteractiveDashboardAgent:
    """
    Агент для построения интерактивного дашборда (MVP версия - статический matplotlib).
    В будущем можно расширить до Plotly/Dash.
    """

    def run(self, tasks: list):
        df = pd.DataFrame(tasks)
        summary = df.groupby("status").size()

        fig, ax = plt.subplots()
        summary.plot(kind="bar", ax=ax, title="Tasks by Status")
        fig.tight_layout()

        return fig













