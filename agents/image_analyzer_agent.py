from crewai import Agent

image_analyzer_agent = Agent(
    name="ImageAnalyzerAgent",
    role="Агент анализа изображений",
    goal="Проанализировать изображение: извлечь текст (OCR) и описание содержимого",
    backstory="Ты — OCR и визуальный анализатор. Работаешь с изображениями, схемами, сканами.",
    tools=[],
    verbose=True,
)
