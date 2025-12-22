"""Create classes and courses tables

Revision ID: 003_create_classes_and_courses
Revises: 002_users_and_childs
Create Date: 2025-12-22 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003_create_classes_and_courses'
down_revision = '002_users_and_childs'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create classes table
    op.create_table(
        'classes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_classes_id', 'id'),
        sa.Index('ix_classes_name', 'name')
    )
    
    # Create courses table with foreign key to classes
    op.create_table(
        'courses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('class_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_courses_id', 'id'),
        sa.Index('ix_courses_class_id', 'class_id')
    )


def downgrade() -> None:
    op.drop_table('courses')
    op.drop_table('classes')
