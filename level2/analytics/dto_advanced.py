








from pydantic import BaseModel, Field
from typing import Tuple, List, Optional, Dict

class EffortForecastAdvancedConfig(BaseModel):
    min_points: int = Field(6, description="Минимальное число точек истории для использования моделей AR/OLS")
    forecast_periods: int = Field(1, description="Сколько шагов прогнозировать вперёд (целое число)")
    freq: str = Field("D", description="Частота временного ряда при ресемплинге (например, 'D','W','M'). Если нет дат — индекс используется как 0..n-1")
    use_ema: bool = Field(True, description="Вычислять EMA и возвращать ее как feature")
    ema_span: int = Field(3, description="span для EMA")
    use_ols: bool = Field(True, description="Использовать OLS (линейная регрессия) для прогноза")
    use_sarimax: bool = Field(False, description="Использовать SARIMAX (ARIMA) если достаточно данных")
    sarimax_order: Tuple[int,int,int] = Field((1,0,0), description="order(p,d,q) для SARIMAX")
    alpha: float = Field(0.05, description="уровень значимости для доверительных интервалов (1-alpha)")
    use_multivariate_ols: bool = Field(True, description="Use multivariate OLS when metadata features available")

class TrendConfigAdvanced(BaseModel):
    min_points: int = Field(6, description="Минимальное число точек для анализа тренда")
    forecast_periods: int = Field(1, description="Сколько шагов прогнозировать вперёд")
    use_sarima: bool = Field(False, description="Использовать SARIMA для анализа тренда")
    sarima_order: Tuple[int,int,int] = Field((1,0,0), description="order(p,d,q) для SARIMA")
    use_exponential: bool = Field(True, description="Использовать экспоненциальное сглаживание")
    alpha: float = Field(0.05, description="уровень значимости для доверительных интервалов")

class RiskConfigAdvanced(BaseModel):
    use_ml: bool = Field(False, description="Использовать машинное обучение для классификации рисков")
    ml_model_path: Optional[str] = Field(None, description="Путь к предобученной модели")
    text_features: List[str] = Field(["description"], description="Текстовые поля для анализа")
    numeric_features: List[str] = Field(["complexity", "priority"], description="Числовые поля для анализа")
    risk_thresholds: Dict[str, float] = Field({"HIGH": 0.75, "MEDIUM": 0.5, "LOW": 0.25}, description="Пороги для классификации рисков")

class DependencyConfigAdvanced(BaseModel):
    max_depth: int = Field(5, description="Максимальная глубина обхода зависимостей")
    visualize: bool = Field(False, description="Создавать визуализацию графа зависимостей")
    output_dir: Optional[str] = Field(None, description="Директория для сохранения визуализаций")

class ForensicConfigAdvanced(BaseModel):
    delay_threshold_ratio: float = Field(0.2, description="Порог задержки для выявления проблем")
    recurrence_threshold: int = Field(3, description="Порог повторения для выявления повторяющихся проблем")
    analyze_text: bool = Field(False, description="Анализировать текстовые поля для выявления проблем")
    text_fields: List[str] = Field(["description", "notes"], description="Текстовые поля для анализа")








