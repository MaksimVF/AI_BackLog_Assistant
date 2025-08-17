

"""add strategic_analysis_snapshots table

Revision ID: 20250217_add_strategic_snapshots
Revises: None
Create Date: 2025-02-17

"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = "20250217_add_strategic_snapshots"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "strategic_analysis_snapshots",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("project_id", sa.String, nullable=False),
        sa.Column("task_id", sa.String, nullable=True),
        sa.Column("method", sa.String, nullable=False),
        sa.Column("score", sa.Float, nullable=True),
        sa.Column("labels", sa.JSON, nullable=True),
        sa.Column("details", sa.JSON, nullable=True),
        sa.Column("config", sa.JSON, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    )
    op.create_index("idx_strategic_snap_project", "strategic_analysis_snapshots", ["project_id"])
    op.create_index("idx_strategic_snap_task", "strategic_analysis_snapshots", ["task_id"])

def downgrade() -> None:
    op.drop_index("idx_strategic_snap_project", table_name="strategic_analysis_snapshots")
    op.drop_index("idx_strategic_snap_task", table_name="strategic_analysis_snapshots")
    op.drop_table("strategic_analysis_snapshots")

