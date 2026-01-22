"""Add detailed profile fields to tutors table.

Revision ID: 017_add_detailed_profile
Revises: 016_create_tutors_table
Create Date: 2026-01-23 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '017_add_detailed_profile'
down_revision = '016_create_tutors_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to tutors table
    op.add_column('tutors', sa.Column('intro_video_thumbnail', sa.String(500), nullable=True))
    op.add_column('tutors', sa.Column('country_of_birth', sa.String(255), nullable=True))
    op.add_column('tutors', sa.Column('is_professional_tutor', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('tutors', sa.Column('is_super_tutor', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('tutors', sa.Column('student_rating', sa.Float(), nullable=False, server_default='0.0'))
    op.add_column('tutors', sa.Column('teaches', sa.String(255), nullable=True))
    op.add_column('tutors', sa.Column('popularity', sa.String(100), nullable=True))
    op.add_column('tutors', sa.Column('popularity_info', sa.Text(), nullable=True))
    op.add_column('tutors', sa.Column('about_me', sa.Text(), nullable=True))
    op.add_column('tutors', sa.Column('professional', sa.Text(), nullable=True))
    op.add_column('tutors', sa.Column('super_tutor', sa.Text(), nullable=True))
    op.add_column('tutors', sa.Column('resume', postgresql.JSON(), nullable=True))
    op.add_column('tutors', sa.Column('student_comments', postgresql.JSON(), nullable=False, server_default='[]'))


def downgrade() -> None:
    # Remove columns from tutors table
    op.drop_column('tutors', 'student_comments')
    op.drop_column('tutors', 'resume')
    op.drop_column('tutors', 'super_tutor')
    op.drop_column('tutors', 'professional')
    op.drop_column('tutors', 'about_me')
    op.drop_column('tutors', 'popularity_info')
    op.drop_column('tutors', 'popularity')
    op.drop_column('tutors', 'teaches')
    op.drop_column('tutors', 'student_rating')
    op.drop_column('tutors', 'is_super_tutor')
    op.drop_column('tutors', 'is_professional_tutor')
    op.drop_column('tutors', 'country_of_birth')
    op.drop_column('tutors', 'intro_video_thumbnail')
