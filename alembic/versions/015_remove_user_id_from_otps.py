"""Remove user_id column from otps table.

Revision ID: 015_remove_user_id_from_otps
Revises: 014_remove_email_unique_constraint
Create Date: 2026-01-10 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '015_remove_user_id_from_otps'
down_revision = '014_remove_email_unique'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop the index on user_id
    op.drop_index('idx_otps_user_id', table_name='otps')
    # Drop the user_id column
    op.drop_column('otps', 'user_id')


def downgrade() -> None:
    # Add back the user_id column
    op.add_column('otps', sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True))
    # Create the index on user_id
    op.create_index('idx_otps_user_id', 'otps', ['user_id'])
