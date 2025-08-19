
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, Numeric
)
from sqlalchemy.orm import relationship, declarative_base

# Create a new Base for third level models
Base = declarative_base()

class ThirdLevelRun(Base):
    __tablename__ = "third_level_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_at = Column(DateTime, default=datetime.utcnow)
    triggered_by = Column(String(255), nullable=True)
    status = Column(String(50), default="completed")

    results = relationship("ThirdLevelResult", back_populates="run", cascade="all, delete-orphan")

class ThirdLevelResult(Base):
    __tablename__ = "third_level_results"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("third_level_runs.id", ondelete="CASCADE"))
    task_id = Column(String(100), nullable=True)  # Use String instead of Integer
    recommendation = Column(String(100), nullable=False)  # 'accelerate' | 'delay' | 'merge' | 'drop'
    explanation = Column(Text, nullable=True)
    confidence = Column(Numeric, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    run = relationship("ThirdLevelRun", back_populates="results")
class DecisionFeedback(Base):
    __tablename__ = "decision_feedback"

    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(Integer, ForeignKey("third_level_results.id", ondelete="CASCADE"))
    user_id = Column(String(255), nullable=True)
    decision = Column(String(20))  # 'accepted' | 'rejected'
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
