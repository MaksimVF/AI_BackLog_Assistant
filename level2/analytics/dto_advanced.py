





from pydantic import BaseModel, Field
from typing import Tuple

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





