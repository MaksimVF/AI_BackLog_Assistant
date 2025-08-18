





















from typing import List, Dict, Any, Type
from config.config import PipelineConfig, AgentConfig
from pipelines.modality_processing_pipeline import ModalityProcessingPipeline
from pipelines.data_manipulation_pipeline import DataManipulationPipeline
from pipelines.data_output_pipeline import DataOutputPipeline
from pipelines.second_level_pipeline import SecondLevelPipeline
import logging

# Настройка логгера
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
        self.modules = {}
        for agent in self.config.agents:
            if agent.enabled:
                try:
                    module_name = agent.name.replace("_", " ").title().replace(" ", "")
                    module_class = globals()[module_name]
                    self.modules[agent.name] = module_class()
                except KeyError:
                    logger.error(f"Module {agent.name} not found")
                except Exception as e:
                    logger.error(f"Error initializing module {agent.name}: {e}")

    async def run(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Запуск пайплайна первого уровня.
        :param tasks: список задач в формате словарей
        :return: словарь с результатами анализа
        """
        results = {}

        # Обработка модальностей
        try:
            cleaned_tasks = await self.modules["modality_processing"].run(tasks)
            results["modality_processing"] = cleaned_tasks
        except Exception as e:
            logger.error(f"Error running modality_processing: {e}")
            results["modality_processing"] = {"error": str(e)}

        # Манипуляция данными
        try:
            manipulated_tasks = await self.modules["data_manipulation"].run(results["modality_processing"])
            results["data_manipulation"] = manipulated_tasks
        except Exception as e:
            logger.error(f"Error running data_manipulation: {e}")
            results["data_manipulation"] = {"error": str(e)}

        # Вывод данных
        try:
            prepared_tasks = await self.modules["data_output"].run(results["data_manipulation"])
            results["data_output"] = prepared_tasks
        except Exception as e:
            logger.error(f"Error running data_output: {e}")
            results["data_output"] = {"error": str(e)}

        # Запуск второго уровня анализа
        try:
            results["second_level"] = await self.modules["second_level"].run(results["data_output"])
        except Exception as e:
            logger.error(f"Error running second_level: {e}")
            results["second_level"] = {"error": str(e)}

        return results























