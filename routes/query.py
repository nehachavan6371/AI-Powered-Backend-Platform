"""Query Routes"""

import uuid
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from models.schemas import QueryRequest, QueryResponse
from app.dependencies import RAGServiceDep

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest, rag_service: RAGServiceDep):
    """Query documents with RAG"""
    try:
        result = await rag_service.query_documents(request.query, top_k=request.top_k)
        
        return QueryResponse(
            id=str(uuid.uuid4()),
            query=request.query,
            answer=result["answer"],
            sources=result["sources"],
            confidence=result["confidence"],
            execution_time_ms=0  # Add timing
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc)
        )


@router.post("/query/stream")
async def stream_query(request: QueryRequest, rag_service: RAGServiceDep):
    """Stream query response"""
    try:
        async def generate():
            async for chunk in rag_service.stream_query_documents(request.query, top_k=request.top_k):
                yield chunk
        
        return StreamingResponse(generate(), media_type="text/event-stream")
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc)
        )


@router.get("/query/{query_id}")
async def get_query(query_id: str):
    """Get query result by ID"""
    # Implementation would fetch from database
    return {"id": query_id, "status": "completed"}
