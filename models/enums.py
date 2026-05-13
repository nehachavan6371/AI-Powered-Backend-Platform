"""Enums"""

from enum import Enum


class QueryStatus(str, Enum):
    """Query status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowStatus(str, Enum):
    """Workflow status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentType(str, Enum):
    """Document type"""
    PDF = "pdf"
    TEXT = "text"
    MARKDOWN = "markdown"
    JSON = "json"


class RoleType(str, Enum):
    """User role type"""
    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"
