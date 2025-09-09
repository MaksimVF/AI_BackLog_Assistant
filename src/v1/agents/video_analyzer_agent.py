from crewai import Agent

video_analyzer_agent = Agent(
    name="VideoAnalyzerAgent",
    role="Агент анализа видеофайлов",
    goal="Извлечь из видео текст, ключевые фразы, визуальные объекты и временные события",
    backstory="Ты — агент, анализирующий видео по ключевым кадрам, субтитрам и сценам.",
    tools=[],
    verbose=True,
)
