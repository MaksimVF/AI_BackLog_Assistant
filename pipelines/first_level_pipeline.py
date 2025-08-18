





















from typing import List, Dict, Any, Type
from config.config import PipelineConfig, AgentConfig
from pipelines.modality_processing_pipeline import ModalityProcessingPipeline
from pipelines.data_manipulation_pipeline import DataManipulationPipeline
from pipelines.data_output_pipeline import DataOutputPipeline
from pipelines.second_level_pipeline import SecondLevelPipeline

class FirstLevelPipeline:
    """
    Первый уровень анализа: базовая обработка задач.
    """

    def __init__(self, config: PipelineConfig = None):
        """
        Инициализация конвейера с конфигурацией.
        :param config: конфигурация конвейера
        """
        if config is None:
            config = PipelineConfig(
                name="first_level",
                agents=[
                    AgentConfig(name="modality_processing", enabled=True),
                    AgentConfig(name="data_manipulation", enabled=True),
                    AgentConfig(name="data_output", enabled=True),
                    AgentConfig(name="second_level", enabled=True)
                ]
            )
        self.config = config
        self.modules = {
            agent.name: globals()[agent.name.replace("_", " ").title().replace(" ", "")]()
            for agent in self.config.agents
            if agent.enabled
        }

    async def run(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Запуск пайплайна первого уровня.
        :param tasks: список задач в формате словарей
        :return: словарь с результатами анализа
        """
        results = {}

        # Обработка модальностей
        cleaned_tasks = await self.modules["modality_processing"].run(tasks)
        results["modality_processing"] = cleaned_tasks

        # Манипуляция данными
        manipulated_tasks = await self.modules["data_manipulation"].run(cleaned_tasks)
        results["data_manipulation"] = manipulated_tasks

        # Вывод данных
        prepared_tasks = await self.modules["data_output"].run(manipulated_tasks)
        results["data_output"] = prepared_tasks

        # Запуск второго уровня анализа
        results["second_level"] = await self.modules["second_level"].run(prepared_tasks)

        return results























