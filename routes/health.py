"""Health Check Routes"""

from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from models.schemas import HealthCheckResponse

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    return HealthCheckResponse(
        status="operational",
        version="1.0.0",
        timestamp=datetime.utcnow()
    )


@router.get("/health/readiness")
async def readiness_check():
    """Readiness probe - checks if service is ready to accept traffic"""
    return {"status": "ready"}


@router.get("/health/liveness")
async def liveness_check():
    """Liveness probe - checks if service is running"""
    return {"status": "alive"}
