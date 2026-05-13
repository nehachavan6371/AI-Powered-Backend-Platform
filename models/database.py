"""SQLAlchemy Database Models"""

from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Float, Integer, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.config import get_settings

Base = declarative_base()
settings = get_settings()

# Create engine
engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow
)

SessionLocal = sessionmaker(bind=engine)


class Document(Base):
    """Document model"""
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    metadata = Column(JSON, default={})
    file_size = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Document {self.id}: {self.filename}>"


class Query(Base):
    """Query history model"""
    __tablename__ = "queries"
    
    id = Column(String, primary_key=True)
    user_id = Column(String)
    query_text = Column(Text, nullable=False)
    answer = Column(Text)
    confidence = Column(Float)
    execution_time_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Query {self.id}: {self.query_text[:50]}..."


class Workflow(Base):
    """Workflow model"""
    __tablename__ = "workflows"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    steps = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Workflow {self.id}: {self.name}>"


class WorkflowExecution(Base):
    """Workflow execution model"""
    __tablename__ = "workflow_executions"
    
    id = Column(String, primary_key=True)
    workflow_id = Column(String, nullable=False)
    input_data = Column(JSON)
    output_data = Column(JSON)
    status = Column(String)  # pending, running, completed, failed
    execution_time_ms = Column(Integer)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    def __repr__(self):
        return f"<WorkflowExecution {self.id}: {self.status}>"


class APIKey(Base):
    """API Key model"""
    __tablename__ = "api_keys"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    key_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime)
    
    def __repr__(self):
        return f"<APIKey {self.id}>"
