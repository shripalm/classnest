"""create_cart_tables

Revision ID: 023_create_cart_tables
Revises: 022_add_coursepick_to_tutors
Create Date: 2026-02-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '023_create_cart_tables'
down_revision = '022_add_coursepick_to_tutors'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create carts table
    op.create_table(
        'carts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_carts_user_id', 'carts', ['user_id'], unique=False)

    # Create cart_items table
    op.create_table(
        'cart_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('cart_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tutor_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('teacher', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('image', sa.String(500), nullable=True),
        sa.Column('price_amount', sa.Float(), nullable=False),
        sa.Column('price_currency', sa.String(10), nullable=False),
        sa.Column('schedule_date', sa.String(10), nullable=False),
        sa.Column('schedule_time', sa.String(5), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=False),
        sa.Column('student', sa.String(255), nullable=False),
        sa.Column('is_favourite', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['cart_id'], ['carts.id'], ),
        sa.ForeignKeyConstraint(['tutor_id'], ['tutors.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_cart_items_cart_id', 'cart_items', ['cart_id'], unique=False)
    op.create_index('idx_cart_items_tutor_id', 'cart_items', ['tutor_id'], unique=False)

    # Create cart_promo_codes table
    op.create_table(
        'cart_promo_codes',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('cart_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('promo_code', sa.String(100), nullable=False),
        sa.Column('discount_amount', sa.Float(), nullable=False),
        sa.Column('discount_percentage', sa.Float(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('applied_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['cart_id'], ['carts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_cart_promo_codes_cart_id', 'cart_promo_codes', ['cart_id'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_cart_promo_codes_cart_id', table_name='cart_promo_codes')
    op.drop_table('cart_promo_codes')
    op.drop_index('idx_cart_items_tutor_id', table_name='cart_items')
    op.drop_index('idx_cart_items_cart_id', table_name='cart_items')
    op.drop_table('cart_items')
    op.drop_index('idx_carts_user_id', table_name='carts')
    op.drop_table('carts')
