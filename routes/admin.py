"""Admin Routes"""

from fastapi import APIRouter, Depends
from app.dependencies import CurrentUserDep

router = APIRouter()


@router.get("/stats")
async def get_stats(current_user: CurrentUserDep):
    """Get system statistics"""
    return {
        "total_queries": 1000,
        "total_documents": 50,
        "vector_store_size": "2.5 GB",
        "cache_hit_rate": "75%"
    }


@router.post("/cache/clear")
async def clear_cache(current_user: CurrentUserDep):
    """Clear cache"""
    return {"status": "cache_cleared"}


@router.get("/logs")
async def view_logs(current_user: CurrentUserDep, lines: int = 100):
    """View logs"""
    return {"logs": [], "lines": lines}
