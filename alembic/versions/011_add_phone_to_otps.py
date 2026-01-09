"""Add phone column to otps table

Revision ID: 011_add_phone_to_otps
Revises: 010_add_verification_fields_to_users
Create Date: 2025-01-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '011_add_phone_to_otps'
down_revision = '010_add_verification_to_users'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('otps', sa.Column('phone', sa.String(20), nullable=True))


def downgrade() -> None:
    op.drop_column('otps', 'phone')
