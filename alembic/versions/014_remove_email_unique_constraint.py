"""Remove unique constraint from email index.

Revision ID: 014_remove_email_unique_constraint
Revises: 013_add_is_verified_back_to_users
Create Date: 2026-01-10 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '014_remove_email_unique'
down_revision = '013_add_is_verified'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop the unique constraint on email
    op.drop_index('idx_users_email', table_name='users')
    # Create non-unique index on email for faster lookups
    op.create_index('idx_users_email', 'users', ['email'], unique=False)


def downgrade() -> None:
    # Restore the unique constraint on email
    op.drop_index('idx_users_email', table_name='users')
    op.create_index('idx_users_email', 'users', ['email'], unique=True)
