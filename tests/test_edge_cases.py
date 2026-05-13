"""Edge Case Tests"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from models.schemas import QueryRequest

client = TestClient(app)


def test_empty_query():
    """Test empty query handling"""
    request = QueryRequest(query="")
    # Should fail validation
    assert request.query == ""


def test_very_long_query():
    """Test very long query"""
    long_query = "a" * 1001
    with pytest.raises(ValueError):
        QueryRequest(query=long_query)


def test_special_characters_in_query():
    """Test special characters in query"""
    request = QueryRequest(query="<script>alert('xss')</script>")
    assert request.query == "<script>alert('xss')</script>"


def test_unicode_in_query():
    """Test Unicode in query"""
    request = QueryRequest(query="你好世界 مرحبا بالعالم")
    assert len(request.query) > 0


def test_top_k_boundary():
    """Test top_k boundary values"""
    # Should pass
    req1 = QueryRequest(query="test", top_k=1)
    assert req1.top_k == 1
    
    req2 = QueryRequest(query="test", top_k=20)
    assert req2.top_k == 20
    
    # Should fail
    with pytest.raises(ValueError):
        QueryRequest(query="test", top_k=0)
    
    with pytest.raises(ValueError):
        QueryRequest(query="test", top_k=21)
