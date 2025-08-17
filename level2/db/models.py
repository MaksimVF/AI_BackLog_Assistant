



from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, text, JSON
from .session import Base

class StrategicAnalysisSnapshot(Base):
    __tablename__ = "strategic_analysis_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    project_id = Column(String, nullable=False)
    task_id = Column(String, nullable=True)
    method = Column(String, nullable=False)
    score = Column(Float, nullable=True)
    labels = Column(JSON, nullable=True)
    details = Column(JSON, nullable=True)
    config = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))



