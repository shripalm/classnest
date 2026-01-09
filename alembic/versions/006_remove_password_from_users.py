"""Remove hashed_password column from users table

Revision ID: 006_remove_password_from_users
Revises: 005_create_otps_table
Create Date: 2025-01-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '006_remove_password_from_users'
down_revision = '005_create_otps_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('users', 'hashed_password')


def downgrade() -> None:
    op.add_column('users', sa.Column('hashed_password', sa.String(255), nullable=False, server_default=''))
