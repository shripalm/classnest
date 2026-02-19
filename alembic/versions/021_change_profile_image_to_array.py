"""Change profile_image to profile_images array.

Revision ID: 021_change_profile_image_to_es
Revises: 020_create_schools_table
Create Date: 2026-02-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '021_change_profile_image_to_es'
down_revision = '020_create_schools_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # For tutors table
    op.drop_column('tutors', 'profile_image')
    op.add_column('tutors', sa.Column('profile_images', postgresql.JSON(), nullable=False, server_default='[]'))
    
    # For schools table
    op.drop_column('schools', 'profile_image')
    op.add_column('schools', sa.Column('profile_images', postgresql.JSON(), nullable=False, server_default='[]'))


def downgrade() -> None:
    # For tutors table
    op.drop_column('tutors', 'profile_images')
    op.add_column('tutors', sa.Column('profile_image', sa.String(500), nullable=True))
    
    # For schools table
    op.drop_column('schools', 'profile_images')
    op.add_column('schools', sa.Column('profile_image', sa.String(500), nullable=True))
