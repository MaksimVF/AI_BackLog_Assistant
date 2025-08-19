
"""add third level tables

Revision ID: 20250819_add_third_level
Revises: 20250801_add_teamwork
Create Date: 2025-08-19
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = "20250819_add_third_level"
down_revision = "20250801_add_teamwork"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "third_level_runs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("run_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("triggered_by", sa.String(255), nullable=True),
        sa.Column("status", sa.String(50), default="completed"),
    )

    op.create_table(
        "third_level_results",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("run_id", sa.Integer, sa.ForeignKey("third_level_runs.id", ondelete="CASCADE")),
        sa.Column("task_id", sa.Integer, sa.ForeignKey("tasks.id", ondelete="CASCADE"), nullable=True),
        sa.Column("recommendation", sa.String(100), nullable=False),
        sa.Column("explanation", sa.Text, nullable=True),
        sa.Column("confidence", sa.Numeric, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "decision_feedback",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("result_id", sa.Integer, sa.ForeignKey("third_level_results.id", ondelete="CASCADE")),
        sa.Column("user_id", sa.String(255), nullable=True),
        sa.Column("decision", sa.String(20)),
        sa.Column("feedback", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

def downgrade():
    op.drop_table("decision_feedback")
    op.drop_table("third_level_results")
    op.drop_table("third_level_runs")
