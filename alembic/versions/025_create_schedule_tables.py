"""create_schedule_tables

Revision ID: 025_create_schedule_tables
Revises: 024_create_calendar_tables
Create Date: 2026-02-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '025_create_schedule_tables'
down_revision = '024_create_calendar_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create tutor_availabilities table
    op.create_table(
        'tutor_availabilities',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tutor_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('timezone', sa.String(100), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=False),
        sa.Column('month', sa.String(20), nullable=False),
        sa.Column('available_dates', postgresql.JSON(), nullable=False),
        sa.Column('time_slots', postgresql.JSON(), nullable=False),
        sa.Column('selected_date_key', sa.String(20), nullable=True),
        sa.Column('selected_slots', postgresql.JSON(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['tutor_id'], ['tutors.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_tutor_availabilities_tutor_id', 'tutor_availabilities', ['tutor_id'], unique=False)
    op.create_index('idx_tutor_availabilities_month', 'tutor_availabilities', ['month'], unique=False)

    # Create time_slots table
    op.create_table(
        'time_slots',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tutor_availability_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tutor_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('slot_id', sa.String(50), nullable=False),
        sa.Column('time', sa.String(5), nullable=False),
        sa.Column('period', sa.String(20), nullable=False),
        sa.Column('is_available', sa.Boolean(), nullable=False),
        sa.Column('is_selected', sa.Boolean(), nullable=False),
        sa.Column('available_dates', postgresql.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['tutor_availability_id'], ['tutor_availabilities.id'], ),
        sa.ForeignKeyConstraint(['tutor_id'], ['tutors.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_time_slots_tutor_availability_id', 'time_slots', ['tutor_availability_id'], unique=False)
    op.create_index('idx_time_slots_tutor_id', 'time_slots', ['tutor_id'], unique=False)
    op.create_index('idx_time_slots_period', 'time_slots', ['period'], unique=False)

    # Create available_dates table
    op.create_table(
        'available_dates',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tutor_availability_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tutor_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('day', sa.String(3), nullable=False),
        sa.Column('date', sa.Integer(), nullable=False),
        sa.Column('date_key', sa.String(10), nullable=False),
        sa.Column('is_today', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['tutor_availability_id'], ['tutor_availabilities.id'], ),
        sa.ForeignKeyConstraint(['tutor_id'], ['tutors.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_available_dates_tutor_availability_id', 'available_dates', ['tutor_availability_id'], unique=False)
    op.create_index('idx_available_dates_tutor_id', 'available_dates', ['tutor_id'], unique=False)
    op.create_index('idx_available_dates_date_key', 'available_dates', ['date_key'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_available_dates_date_key', table_name='available_dates')
    op.drop_index('idx_available_dates_tutor_id', table_name='available_dates')
    op.drop_index('idx_available_dates_tutor_availability_id', table_name='available_dates')
    op.drop_table('available_dates')
    op.drop_index('idx_time_slots_period', table_name='time_slots')
    op.drop_index('idx_time_slots_tutor_id', table_name='time_slots')
    op.drop_index('idx_time_slots_tutor_availability_id', table_name='time_slots')
    op.drop_table('time_slots')
    op.drop_index('idx_tutor_availabilities_month', table_name='tutor_availabilities')
    op.drop_index('idx_tutor_availabilities_tutor_id', table_name='tutor_availabilities')
    op.drop_table('tutor_availabilities')
