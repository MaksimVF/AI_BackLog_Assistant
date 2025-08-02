
class BaseAgent:
    def __init__(self, name=None):
        self.name = name

    def log(self, message, level="info"):
        print(f"[{self.name}] [{level.upper()}] {message}")

    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"
