"""Pydantic Schemas"""

from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel, Field


# Query Schemas
class QueryRequest(BaseModel):
    """Query request schema"""
    query: str = Field(..., min_length=1, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=20)
    include_metadata: bool = False


class QueryResponse(BaseModel):
    """Query response schema"""
    id: str
    query: str
    answer: str
    sources: List[dict]
    confidence: float
    execution_time_ms: int


# Document Schemas
class DocumentMetadata(BaseModel):
    """Document metadata"""
    filename: Optional[str] = None
    file_type: Optional[str] = None
    created_at: Optional[datetime] = None
    source: Optional[str] = None


class DocumentUploadResponse(BaseModel):
    """Document upload response"""
    document_id: str
    filename: str
    size: int
    status: str


class DocumentListResponse(BaseModel):
    """Document list response"""
    total: int
    documents: List[dict]


# Workflow Schemas
class WorkflowStep(BaseModel):
    """Workflow step"""
    name: str
    type: str  # "query", "transform", "filter", etc.
    config: dict


class WorkflowCreateRequest(BaseModel):
    """Workflow create request"""
    name: str
    description: Optional[str] = None
    steps: List[WorkflowStep]


class WorkflowExecuteRequest(BaseModel):
    """Workflow execute request"""
    input_data: dict


class WorkflowExecuteResponse(BaseModel):
    """Workflow execute response"""
    workflow_id: str
    execution_id: str
    status: str
    output: dict
    execution_time_ms: int


# Error Schemas
class ErrorResponse(BaseModel):
    """Error response"""
    detail: str
    error_code: Optional[str] = None
    request_id: Optional[str] = None


# Health Check Schemas
class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime
    checks: Optional[dict] = None
