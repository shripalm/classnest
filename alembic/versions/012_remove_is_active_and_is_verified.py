"""Remove is_active and is_verified columns from users table.

Revision ID: 012_remove_cols
Revises: 011_add_phone_to_otps
Create Date: 2026-01-10 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '012_remove_cols'
down_revision = '011_add_phone_to_otps'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Remove is_active and is_verified columns
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'is_verified')


def downgrade() -> None:
    # Add back is_active and is_verified columns
    op.add_column('users', sa.Column('is_active', sa.Boolean(), server_default=sa.true(), nullable=False))
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), server_default=sa.false(), nullable=False))
