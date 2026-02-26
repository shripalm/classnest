"""Refactor classes to courses and rename courses to subjects

Revision ID: 026_ref_classes_to_courses
Revises: 025_create_schedule_tables
Create Date: 2026-02-25 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '026_ref_classes_to_courses'
down_revision = '025_create_schedule_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Rename 'courses' table to 'subjects'
    op.rename_table('courses', 'subjects')
    
    # Rename 'name' column to 'subject_name' in subjects table
    op.alter_column('subjects', 'name', new_column_name='subject_name')
    
    # Drop the old foreign key constraint before renaming columns
    op.drop_constraint('courses_class_id_fkey', 'subjects', type_='foreignkey')
    
    # Rename 'class_id' to 'course_id' in subjects table
    op.alter_column('subjects', 'class_id', new_column_name='course_id')
    
    # Rename 'classes' table to 'courses' BEFORE creating the new foreign key
    op.rename_table('classes', 'courses')
    
    # Now create the new foreign key constraint
    op.create_foreign_key('subjects_course_id_fkey', 'subjects', 'courses', ['course_id'], ['id'])


def downgrade() -> None:
    # Drop the new foreign key constraint
    op.drop_constraint('subjects_course_id_fkey', 'subjects', type_='foreignkey')
    
    # Rename 'courses' table back to 'classes'
    op.rename_table('courses', 'classes')
    
    # Rename 'course_id' back to 'class_id' in subjects table
    op.alter_column('subjects', 'course_id', new_column_name='class_id')
    
    # Recreate the old foreign key constraint
    op.create_foreign_key('courses_class_id_fkey', 'subjects', 'classes', ['class_id'], ['id'])
    
    # Rename 'subject_name' column back to 'name' in subjects table
    op.alter_column('subjects', 'subject_name', new_column_name='name')
    
    # Rename 'subjects' table back to 'courses'
    op.rename_table('subjects', 'courses')
