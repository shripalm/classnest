"""Remove username column from users table

Revision ID: 008_remove_username_from_users
Revises: 006_remove_password_from_users
Create Date: 2025-01-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '008_remove_username_from_users'
down_revision = '006_remove_password_from_users'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_index('idx_users_username', table_name='users')
    op.drop_column('users', 'username')


def downgrade() -> None:
    op.add_column('users', sa.Column('username', sa.String(50), nullable=False, server_default=''))
    op.create_index('idx_users_username', 'users', ['username'], unique=True)
