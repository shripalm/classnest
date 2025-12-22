"""Create users and children tables

Revision ID: 002_users_and_childs
Revises: 001_create_users_table
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_users_and_childs'
down_revision = '001_create_users_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table with additional fields
    op.add_column('users', sa.Column('name', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('country_code', sa.String(5), nullable=True))
    op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))
    op.add_column('users', sa.Column('address', sa.String(500), nullable=True))
    op.add_column('users', sa.Column('terms_accepted', sa.Boolean(), nullable=False, server_default='false'))
    
    # Create children table
    op.create_table(
        'children',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('parent_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=False),
        sa.Column('gender', sa.String(20), nullable=True),
        sa.Column('photo', sa.String(500), nullable=True),
        sa.Column('interest', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['parent_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_children_parent_id', 'children', ['parent_id'], unique=False)


def downgrade() -> None:
    # Drop children table
    op.drop_index('idx_children_parent_id', table_name='children')
    op.drop_table('children')
    
    # Remove columns from users table
    op.drop_column('users', 'terms_accepted')
    op.drop_column('users', 'address')
    op.drop_column('users', 'phone')
    op.drop_column('users', 'country_code')
    op.drop_column('users', 'name')
