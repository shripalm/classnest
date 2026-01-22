"""Create favorite_tutors table.

Revision ID: 018_create_favorite_tutors_table
Revises: 017_add_detailed_profile
Create Date: 2026-01-23 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '018_create_favorite_tutors_table'
down_revision = '017_add_detailed_profile'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create favorite_tutors table
    op.create_table(
        'favorite_tutors',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tutor_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['tutor_id'], ['tutors.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # Create indexes
    op.create_index('idx_favorite_tutors_user_id', 'favorite_tutors', ['user_id'])
    op.create_index('idx_favorite_tutors_tutor_id', 'favorite_tutors', ['tutor_id'])
    op.create_index('idx_favorite_tutors_user_tutor', 'favorite_tutors', ['user_id', 'tutor_id'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_favorite_tutors_user_tutor', table_name='favorite_tutors')
    op.drop_index('idx_favorite_tutors_tutor_id', table_name='favorite_tutors')
    op.drop_index('idx_favorite_tutors_user_id', table_name='favorite_tutors')
    # Drop table
    op.drop_table('favorite_tutors')
