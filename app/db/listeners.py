import logging
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool

logger = logging.getLogger(__name__)

def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Log SQL statements before execution."""
    logger.debug("EXECUTE SQL: %s", statement)


def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Log SQL statements after execution."""
    pass
