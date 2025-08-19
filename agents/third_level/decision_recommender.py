

from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Note: Task and SecondLevelResult models are not available
# We'll use task_id as string and mock second level data for now

from db_third_level import ThirdLevelRun, ThirdLevelResult as TLResult

class DecisionRecommenderAgent:
    """
    MVP-агент формирует рекомендации на основе сигналов второго уровня и метаданных задач.
    Эвристики:
      - Высокий WSJF или RICE при низком риске → accelerate
      - Низкий скор + высокий риск → delay
      - Очень низкая ценность → drop
      - Похожие задачи по цели/фиче → merge
    """

    def __init__(self,
                 rice_threshold: float = 7.5,
                 wsjf_threshold: float = 7.0,
                 risk_delay_threshold: float = 0.7,
                 low_value_threshold: float = 1.5):
        self.rice_threshold = rice_threshold
        self.wsjf_threshold = wsjf_threshold
        self.risk_delay_threshold = risk_delay_threshold
        self.low_value_threshold = low_value_threshold

    async def _load_signals(self, session: AsyncSession) -> Dict[str, Dict]:
        """
        Собирает сигналы из second_level_results, сгружая по task_id.
        Ожидаемые ключи, если присутствуют:
         - 'scores': {'RICE': float, 'WSJF': float, ...}
         - 'risk': {'level': float}  # 0..1
         - 'value': float, 'effort': float
        """
        # Mock data for testing since SecondLevelResult is not available
        task_signals = {
            "task_123": {
                "scores": {"RICE": 7.2, "WSJF": 8.5},
                "risk": {"level": 0.3},
                "value": 10.0,
                "effort": 3.0
            },
            "task_456": {
                "scores": {"RICE": 5.1, "WSJF": 6.0},
                "risk": {"level": 0.7},
                "value": 6.0,
                "effort": 4.0
            },
            "task_789": {
                "scores": {"RICE": 2.0, "WSJF": 3.0},
                "risk": {"level": 0.9},
                "value": 2.0,
                "effort": 5.0
            }
        }
        return task_signals

    def _decide(self, meta: Dict) -> Optional[Dict]:
        """
        Принимает метаданные по задаче (scores, risk, value/effort), возвращает рекомендацию.
        """
        scores = meta.get("scores", {})
        rice = float(scores.get("RICE") or 0)
        wsjf = float(scores.get("WSJF") or 0)
        risk_level = float((meta.get("risk") or {}).get("level") or 0)
        value = float(meta.get("value") or 0)
        effort = float(meta.get("effort") or 0)

        # accelerate
        if (rice >= self.rice_threshold) or (wsjf >= self.wsjf_threshold):
            if risk_level <= 0.5:
                return dict(recommendation="accelerate",
                          explanation="High RICE/WSJF score with low risk",
                          confidence=0.9)

        # delay
        if (rice <= self.rice_threshold) and (risk_level >= self.risk_delay_threshold):
            return dict(recommendation="delay",
                      explanation="Low RICE with high risk",
                      confidence=0.7)

        # drop
        if value <= self.low_value_threshold:
            return dict(recommendation="drop",
                      explanation="Very low value",
                      confidence=0.8)

        # merge (simplified for MVP)
        if "feature" in meta.get("tags", []):
            return dict(recommendation="merge",
                      explanation="Similar feature tasks",
                      confidence=0.6)

        return None

    async def run(self, session: AsyncSession, triggered_by: str = "system") -> int:
        """
        Запускает процесс рекомендаций, сохраняет результаты в БД.
        Возвращает ID созданного ThirdLevelRun.
        """
        # Create a new run
        run = ThirdLevelRun(triggered_by=triggered_by, status="running")
        session.add(run)
        await session.commit()
        await session.refresh(run)

        # Load signals
        signals = await self._load_signals(session)

        # Process each task
        results = []
        for task_id, meta in signals.items():
            decision = self._decide(meta)
            if decision:
                result = TLResult(
                    run_id=run.id,
                    task_id=task_id,
                    recommendation=decision["recommendation"],
                    explanation=decision["explanation"],
                    confidence=decision["confidence"]
                )
                session.add(result)
                results.append(result)

        # Update run status
        run.status = "completed"
        await session.commit()
        await session.refresh(run)

        return run.id

