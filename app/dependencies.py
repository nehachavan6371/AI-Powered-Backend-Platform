"""Dependency Injection"""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
import jwt

from app.config import get_settings
from services.llm_service import LLMService
from services.rag_service import RAGService
from services.vector_store_service import VectorStoreService

security = HTTPBearer()
settings = get_settings()


async def verify_token(credentials: Annotated[HTTPAuthCredentials, Depends(security)]) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )


async def get_llm_service() -> LLMService:
    """Get LLM service instance"""
    return LLMService()


async def get_rag_service() -> RAGService:
    """Get RAG service instance"""
    return RAGService()


async def get_vector_store_service() -> VectorStoreService:
    """Get vector store service instance"""
    return VectorStoreService()


# Type annotations
LLMServiceDep = Annotated[LLMService, Depends(get_llm_service)]
RAGServiceDep = Annotated[RAGService, Depends(get_rag_service)]
VectorStoreServiceDep = Annotated[VectorStoreService, Depends(get_vector_store_service)]
CurrentUserDep = Annotated[dict, Depends(verify_token)]
