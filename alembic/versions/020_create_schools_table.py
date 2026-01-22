"""Create schools table.

Revision ID: 020_create_schools_table
Revises: 019_add_times_and_days
Create Date: 2026-01-23 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '020_create_schools_table'
down_revision = '019_add_times_and_days'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create schools table
    op.create_table(
        'schools',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('profile_image', sa.String(500), nullable=True),
        sa.Column('intro_video_thumbnail', sa.String(500), nullable=True),
        sa.Column('country_flag', sa.String(500), nullable=True),
        sa.Column('flag', sa.String(500), nullable=True),
        sa.Column('country_of_birth', sa.String(255), nullable=True),
        sa.Column('about_us', sa.Text(), nullable=True),
        sa.Column('verified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_professional_tutor', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_super_tutor', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('badge', sa.String(100), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(10), nullable=False, server_default='SGD'),
        sa.Column('lesson_duration', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('student_rating', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('is_favourite', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('reviews', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('headline', sa.Text(), nullable=True),
        sa.Column('teaches', sa.String(255), nullable=True),
        sa.Column('popularity', sa.String(100), nullable=True),
        sa.Column('popularity_info', sa.Text(), nullable=True),
        sa.Column('students', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('lessons', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('professional', sa.Text(), nullable=True),
        sa.Column('super_tutor', sa.Text(), nullable=True),
        sa.Column('languages', postgresql.JSON(), nullable=False, server_default='[]'),
        sa.Column('coursepick', postgresql.JSON(), nullable=False, server_default='[]'),
        sa.Column('resume', postgresql.JSON(), nullable=True),
        sa.Column('student_comments', postgresql.JSON(), nullable=False, server_default='[]'),
        sa.Column('times_available', postgresql.JSON(), nullable=False, server_default='[]'),
        sa.Column('days_available', postgresql.JSON(), nullable=False, server_default='[]'),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    # Create indexes
    op.create_index('idx_schools_name', 'schools', ['name'])
    op.create_index('idx_schools_verified', 'schools', ['verified'])
    op.create_index('idx_schools_rating', 'schools', ['rating'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_schools_rating', 'schools')
    op.drop_index('idx_schools_verified', 'schools')
    op.drop_index('idx_schools_name', 'schools')
    # Drop table
    op.drop_table('schools')
