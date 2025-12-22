from enum import Enum


class UserRole(str, Enum):
    """User roles enumeration."""
    ADMIN = "admin"
    INSTRUCTOR = "instructor"
    STUDENT = "student"
    PARENT = "parent"


class UserStatus(str, Enum):
    """User status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"
