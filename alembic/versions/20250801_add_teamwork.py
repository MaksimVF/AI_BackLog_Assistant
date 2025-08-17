


"""add teamwork tables

Revision ID: 20250801_add_teamwork
Revises: 20250217_add_strategic_snapshots
Create Date: 2025-08-01
"""
from alembic import op
import sqlalchemy as sa

revision = "20250801_add_teamwork"
down_revision = "20250217_add_strategic_snapshots"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "voting_records",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("project_id", sa.String, nullable=False),
        sa.Column("task_id", sa.String, nullable=False),
        sa.Column("votes", sa.JSON, nullable=False),
        sa.Column("result", sa.JSON, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    )
    op.create_table(
        "conflict_records",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("project_id", sa.String, nullable=False),
        sa.Column("task_id", sa.String, nullable=True),
        sa.Column("analysis", sa.JSON, nullable=True),
        sa.Column("severity", sa.Float, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    )
    op.create_table(
        "stakeholder_alignment",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("project_id", sa.String, nullable=False),
        sa.Column("task_id", sa.String, nullable=True),
        sa.Column("score", sa.Float, nullable=True),
        sa.Column("details", sa.JSON, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    )

def downgrade():
    op.drop_table("stakeholder_alignment")
    op.drop_table("conflict_records")
    op.drop_table("voting_records")


