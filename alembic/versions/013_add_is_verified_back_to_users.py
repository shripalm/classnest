"""Add is_verified column back to users table.

Revision ID: 013_add_is_verified_back_to_users
Revises: 012_remove_is_active_and_is_verified
Create Date: 2026-01-10 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '013_add_is_verified'
down_revision = '012_remove_cols'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add is_verified column to users table
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), server_default=sa.false(), nullable=False))


def downgrade() -> None:
    # Drop is_verified column from users table
    op.drop_column('users', 'is_verified')
