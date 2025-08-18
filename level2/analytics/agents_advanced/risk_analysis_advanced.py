









import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, Any, Tuple, Optional
from level2.dto import Task
from ..dto_advanced import RiskConfigAdvanced
from ..utils import safe_float
import pickle
import os

class RiskAnalysisAdvancedAgent:
    name = "RISK_ANALYSIS_ADV"

    def __init__(self, model_path: Optional[str] = None):
        self.vectorizer = TfidfVectorizer(max_features=100)
        self.model = RandomForestClassifier()
        self.model_path = model_path
        if model_path and os.path.exists(model_path):
            self.load_model()

    def load_model(self):
        if not self.model_path:
            return
        with open(self.model_path, "rb") as f:
            data = pickle.load(f)
        self.model = data["model"]
        self.vectorizer = data["vectorizer"]

    def save_model(self):
        if not self.model_path:
            return
        with open(self.model_path, "wb") as f:
            pickle.dump({"model": self.model, "vectorizer": self.vectorizer}, f)

    def _train_model(self, tasks: list):
        # Обучение модели на исторических данных
        texts = []
        for t in tasks:
            text_parts = []
            for field in self.vectorizer.get_feature_names_out():
                text_parts.append(str(t.metadata.get(field, "")))
            texts.append(" ".join(text_parts))
        X = self.vectorizer.fit_transform(texts)
        y = [t.metadata.get("risk_level", "LOW") for t in tasks]
        self.model.fit(X, y)
        self.save_model()

    def score(self, task: Task, cfg: RiskConfigAdvanced) -> Tuple[float, Dict[str, Any], Dict[str, str]]:
        # Анализ текста задачи
        text_parts = []
        for field in cfg.text_features:
            text_parts.append(str(task.metadata.get(field, "")))
        text = " ".join(text_parts)

        # Преобразование текста
        X = self.vectorizer.transform([text])

        # Прогноз риска
        risk_level = self.model.predict(X)[0]

        # Дополнительные факторы
        details = {
            "risk_level": risk_level,
            "features": dict(zip(self.vectorizer.get_feature_names_out(), X.toarray()[0]))
        }

        # Оценка риска
        risk_score = cfg.risk_thresholds.get(risk_level, 0.5)

        return risk_score, details, {"RISK_LEVEL": risk_level}









