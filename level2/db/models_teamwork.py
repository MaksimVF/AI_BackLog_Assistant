




from sqlalchemy import Column, BigInteger, String, TIMESTAMP, text, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class VotingRecord(Base):
    __tablename__ = "voting_records"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    project_id = Column(String, nullable=False)
    task_id = Column(String, nullable=False)
    votes = Column(JSONB, nullable=False)
    result = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

class ConflictRecord(Base):
    __tablename__ = "conflict_records"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    project_id = Column(String, nullable=False)
    task_id = Column(String, nullable=True)
    analysis = Column(JSONB, nullable=True)
    severity = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

class StakeholderAlignmentRecord(Base):
    __tablename__ = "stakeholder_alignment"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    project_id = Column(String, nullable=False)
    task_id = Column(String, nullable=True)
    score = Column(Float, nullable=True)
    details = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

class PredictiveAnalysisSnapshot(Base):
    __tablename__ = "predictive_analysis_snapshots"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    project_id = Column(String, nullable=True)
    task_id = Column(String, nullable=True)
    agent = Column(String, nullable=False)
    score = Column(Float, nullable=True)
    details = Column(JSONB, nullable=True)
    labels = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))




