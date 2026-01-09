"""Remove redundant name column from users table

Revision ID: 009_remove_name_from_users
Revises: 008_remove_username_from_users
Create Date: 2025-01-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '009_remove_name_from_users'
down_revision = '008_remove_username_from_users'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('users', 'name')


def downgrade() -> None:
    op.add_column('users', sa.Column('name', sa.String(255), nullable=True))
