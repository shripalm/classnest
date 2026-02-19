"""create_calendar_tables

Revision ID: 024_create_calendar_tables
Revises: 023_create_cart_tables
Create Date: 2026-02-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '024_create_calendar_tables'
down_revision = '023_create_cart_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create calendar_events table
    op.create_table(
        'calendar_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('event_date', sa.String(10), nullable=False),
        sa.Column('event_id', sa.String(100), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('color', sa.String(20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_calendar_events_user_id', 'calendar_events', ['user_id'], unique=False)
    op.create_index('idx_calendar_events_event_date', 'calendar_events', ['event_date'], unique=False)
    op.create_index('idx_calendar_events_user_date', 'calendar_events', ['user_id', 'event_date'], unique=False)

    # Create daily_schedules table
    op.create_table(
        'daily_schedules',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('schedule_date', sa.String(10), nullable=False),
        sa.Column('class_id', sa.String(100), nullable=False),
        sa.Column('start_time', sa.String(5), nullable=False),
        sa.Column('end_time', sa.String(5), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('students', postgresql.JSON(), nullable=False),
        sa.Column('student_colors', postgresql.JSON(), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('can_reschedule', sa.Boolean(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_daily_schedules_user_id', 'daily_schedules', ['user_id'], unique=False)
    op.create_index('idx_daily_schedules_schedule_date', 'daily_schedules', ['schedule_date'], unique=False)
    op.create_index('idx_daily_schedules_user_date', 'daily_schedules', ['user_id', 'schedule_date'], unique=False)

    # Create calendar_months table
    op.create_table(
        'calendar_months',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('month', sa.String(7), nullable=False),
        sa.Column('today', sa.String(10), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_calendar_months_user_id', 'calendar_months', ['user_id'], unique=False)
    op.create_index('idx_calendar_months_month', 'calendar_months', ['month'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_calendar_months_month', table_name='calendar_months')
    op.drop_index('idx_calendar_months_user_id', table_name='calendar_months')
    op.drop_table('calendar_months')
    op.drop_index('idx_daily_schedules_user_date', table_name='daily_schedules')
    op.drop_index('idx_daily_schedules_schedule_date', table_name='daily_schedules')
    op.drop_index('idx_daily_schedules_user_id', table_name='daily_schedules')
    op.drop_table('daily_schedules')
    op.drop_index('idx_calendar_events_user_date', table_name='calendar_events')
    op.drop_index('idx_calendar_events_event_date', table_name='calendar_events')
    op.drop_index('idx_calendar_events_user_id', table_name='calendar_events')
    op.drop_table('calendar_events')
