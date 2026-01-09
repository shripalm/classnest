"""Create OTPs table

Revision ID: 005_create_otps_table
Revises: 004_add_soft_delete_to_users
Create Date: 2025-01-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '005_create_otps_table'
down_revision = '004_add_soft_delete_to_users'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'otps',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('otp_code', sa.String(10), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('attempts', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('verified_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_otps_email', 'otps', ['email'], unique=False)
    op.create_index('idx_otps_user_id', 'otps', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_otps_user_id', table_name='otps')
    op.drop_index('idx_otps_email', table_name='otps')
    op.drop_table('otps')
