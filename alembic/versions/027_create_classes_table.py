"""Create classes table

Revision ID: 027_create_classes_table
Revises: 026_ref_classes_to_courses
Create Date: 2026-03-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '027_create_classes_table'
down_revision = '026_ref_classes_to_courses'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'classes',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
        sa.Column('class_name', sa.String(256), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('course_name', sa.String(256), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=False),
        sa.Column('subject_name', sa.String(256), nullable=False),
        sa.Column('tutor_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('institute_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('tutor_institute_name', sa.String(256), nullable=False),
        sa.Column('location', sa.String(256), nullable=False),
        sa.Column('description', sa.String(1024), nullable=False),
        sa.Column('runtime_per_session_min', sa.Integer(), nullable=False),
        sa.Column('total_sessions', sa.Integer(), nullable=True),
        sa.Column('cost', sa.Float(), nullable=False),
        sa.Column('duration', sa.String(64), nullable=False),
        sa.Column('min_age', sa.Integer(), nullable=False),
        sa.Column('max_age', sa.Integer(), nullable=False),
        sa.Column('default_reviews_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('default_rating', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('is_deleted', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ),
        sa.ForeignKeyConstraint(['tutor_id'], ['tutors.id'], ),
        sa.ForeignKeyConstraint(['institute_id'], ['schools.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_classes_course_id', 'classes', ['course_id'], unique=False)
    op.create_index('idx_classes_subject_id', 'classes', ['subject_id'], unique=False)
    op.create_index('idx_classes_tutor_id', 'classes', ['tutor_id'], unique=False)
    op.create_index('idx_classes_institute_id', 'classes', ['institute_id'], unique=False)
    op.create_index('idx_classes_location', 'classes', ['location'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_classes_location', table_name='classes')
    op.drop_index('idx_classes_institute_id', table_name='classes')
    op.drop_index('idx_classes_tutor_id', table_name='classes')
    op.drop_index('idx_classes_subject_id', table_name='classes')
    op.drop_index('idx_classes_course_id', table_name='classes')
    op.drop_table('classes')
