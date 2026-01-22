"""Add times_available and days_available to tutors table.

Revision ID: 019_add_times_and_days
Revises: 018_create_favorite_tutors_table
Create Date: 2026-01-23 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '019_add_times_and_days'
down_revision = '018_create_favorite_tutors_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to tutors table
    op.add_column('tutors', sa.Column('times_available', postgresql.JSON(), nullable=False, server_default='[]'))
    op.add_column('tutors', sa.Column('days_available', postgresql.JSON(), nullable=False, server_default='[]'))


def downgrade() -> None:
    # Remove columns
    op.drop_column('tutors', 'days_available')
    op.drop_column('tutors', 'times_available')
