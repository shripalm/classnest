"""Add soft delete fields to users table.

Revision ID: 004_add_soft_delete_to_users
Revises: 003_create_classes_and_courses
Create Date: 2026-01-05 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004_add_soft_delete_to_users'
down_revision = '003_create_classes_and_courses'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add is_deleted column with default value False
    op.add_column('users', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'))
    # Add deleted_at column to track when user was deleted
    op.add_column('users', sa.Column('deleted_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    # Remove columns if migration is rolled back
    op.drop_column('users', 'deleted_at')
    op.drop_column('users', 'is_deleted')
