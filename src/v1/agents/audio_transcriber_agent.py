from crewai import Agent

audio_transcriber_agent = Agent(
    name="AudioTranscriberAgent",
    role="Агент транскрипции аудио",
    goal="Конвертировать речь из аудиофайла в текстовую форму (ASR)",
    backstory="Ты — распознаватель речи. Принимаешь аудиофайлы и возвращаешь точный текст.",
    tools=[],
    verbose=True,
)
