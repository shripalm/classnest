"""Create tutors table.

Revision ID: 016_create_tutors_table
Revises: 015_remove_user_id_from_otps
Create Date: 2026-01-23 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '016_create_tutors_table'
down_revision = '015_remove_user_id_from_otps'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create tutors table
    op.create_table(
        'tutors',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('profile_image', sa.String(500), nullable=True),
        sa.Column('country_flag', sa.String(500), nullable=True),
        sa.Column('verified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('badge', sa.String(100), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(10), nullable=False, server_default='SGD'),
        sa.Column('lesson_duration', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('is_favourite', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('reviews', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('headline', sa.Text(), nullable=True),
        sa.Column('students', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('lessons', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('languages', postgresql.JSON(), nullable=False, server_default='[]'),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    # Create indexes
    op.create_index('idx_tutors_name', 'tutors', ['name'])
    op.create_index('idx_tutors_verified', 'tutors', ['verified'])
    op.create_index('idx_tutors_rating', 'tutors', ['rating'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_tutors_rating', table_name='tutors')
    op.drop_index('idx_tutors_verified', table_name='tutors')
    op.drop_index('idx_tutors_name', table_name='tutors')
    # Drop table
    op.drop_table('tutors')
