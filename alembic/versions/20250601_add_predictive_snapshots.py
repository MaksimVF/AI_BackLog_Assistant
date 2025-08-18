





"""add predictive_analysis_snapshots table

Revision ID: 20250601_add_predictive_snapshots
Revises: <prev_revision_id>
Create Date: 2025-06-01
"""
from alembic import op
import sqlalchemy as sa

revision = "20250601_add_predictive_snapshots"
down_revision = "<prev_revision_id>"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "predictive_analysis_snapshots",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("project_id", sa.String, nullable=True),
        sa.Column("task_id", sa.String, nullable=True),
        sa.Column("agent", sa.String, nullable=False),
        sa.Column("score", sa.Float, nullable=True),
        sa.Column("details", sa.dialects.postgresql.JSONB, nullable=True),
        sa.Column("labels", sa.dialects.postgresql.JSONB, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    )
    op.create_index("idx_predictive_proj", "predictive_analysis_snapshots", ["project_id"])
    op.create_index("idx_predictive_task", "predictive_analysis_snapshots", ["task_id"])

def downgrade():
    op.drop_index("idx_predictive_task", table_name="predictive_analysis_snapshots")
    op.drop_index("idx_predictive_proj", table_name="predictive_analysis_snapshots")
    op.drop_table("predictive_analysis_snapshots")





