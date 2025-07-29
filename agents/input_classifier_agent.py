from crewai import Agent
from tools.file_type_detector import FileTypeDetectorTool

file_type_detector = FileTypeDetectorTool()

InputClassifierAgent = Agent(
    role="Классификатор входной информации",
    goal="Определять тип входных данных и вызывать соответствующие инструменты обработки",
    tools=[
        file_type_detector  # временно только этот, остальные позже
    ],
    verbose=True,
    allow_delegation=True
)
