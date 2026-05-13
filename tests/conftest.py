"""Pytest Configuration"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import Settings
from unittest.mock import Mock, AsyncMock


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
def mock_settings():
    """Mock settings"""
    settings = Settings(
        openai_api_key="test-key",
        database_url="sqlite:///:memory:",
        secret_key="test-secret"
    )
    return settings


@pytest.fixture
def mock_llm_service():
    """Mock LLM service"""
    service = AsyncMock()
    service.generate_response = AsyncMock(return_value="Test response")
    service.generate_embedding = AsyncMock(return_value=[0.1] * 1536)
    return service


@pytest.fixture
def mock_rag_service():
    """Mock RAG service"""
    service = AsyncMock()
    service.query_documents = AsyncMock(return_value={
        "answer": "Test answer",
        "sources": [],
        "confidence": 0.95
    })
    return service
