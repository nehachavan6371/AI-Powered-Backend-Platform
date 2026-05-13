"""API Endpoint Tests"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "operational"


def test_readiness_check():
    """Test readiness check endpoint"""
    response = client.get("/health/readiness")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_liveness_check():
    """Test liveness check endpoint"""
    response = client.get("/health/liveness")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "docs" in data
