"""Add coursepick to tutors table.

Revision ID: 022_add_coursepick_to_tutors
Revises: 021_change_profile_image_to_es
Create Date: 2026-02-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '022_add_coursepick_to_tutors'
down_revision = '021_change_profile_image_to_es'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add coursepick column to tutors table
    op.add_column('tutors', sa.Column('coursepick', postgresql.JSON(), nullable=False, server_default='[]'))


def downgrade() -> None:
    # Remove coursepick column from tutors table
    op.drop_column('tutors', 'coursepick')
