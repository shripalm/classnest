"""Add is_email_verified and is_phone_verified columns to users table

Revision ID: 010_add_verification_fields_to_users
Revises: 009_remove_name_from_users
Create Date: 2025-01-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '010_add_verification_to_users'
down_revision = '009_remove_name_from_users'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_email_verified', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('users', sa.Column('is_phone_verified', sa.Boolean(), nullable=False, server_default='false'))


def downgrade() -> None:
    op.drop_column('users', 'is_phone_verified')
    op.drop_column('users', 'is_email_verified')
