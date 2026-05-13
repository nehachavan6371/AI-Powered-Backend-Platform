"""RAG Service - Retrieval Augmented Generation"""

import logging
from typing import List, Optional
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

from app.config import get_settings
from services.llm_service import LLMService
from services.vector_store_service import VectorStoreService
from rag.pipeline import RAGPipeline
from rag.output_validators import OutputValidator

logger = logging.getLogger(__name__)
settings = get_settings()


class RAGService:
    """RAG Service for retrieval and generation"""

    def __init__(self):
        """Initialize RAG service"""
        self.llm_service = LLMService()
        self.vector_store_service = VectorStoreService()
        self.pipeline = RAGPipeline()
        self.validator = OutputValidator()

    async def query_documents(self, query: str, top_k: int = 5) -> dict:
        """Query documents with RAG"""
        try:
            # Retrieve relevant documents
            documents = await self.vector_store_service.search(query, top_k=top_k)
            
            if not documents:
                return {
                    "answer": "No relevant documents found.",
                    "sources": [],
                    "confidence": 0.0
                }
            
            # Generate context from retrieved documents
            context = self._create_context(documents)
            
            # Generate response
            answer = await self.llm_service.generate_response(query, context=context)
            
            # Validate output
            validated_answer = self.validator.validate(answer)
            
            return {
                "answer": validated_answer,
                "sources": documents,
                "confidence": self._calculate_confidence(documents)
            }
        
        except Exception as exc:
            logger.error(f"Error querying documents: {exc}")
            raise

    async def stream_query_documents(self, query: str, top_k: int = 5):
        """Stream query results"""
        try:
            documents = await self.vector_store_service.search(query, top_k=top_k)
            context = self._create_context(documents)
            
            async for chunk in self.llm_service.stream_response(query, context=context):
                yield chunk
        
        except Exception as exc:
            logger.error(f"Error streaming query: {exc}")
            raise

    def _create_context(self, documents: List[dict]) -> str:
        """Create context from documents"""
        context_parts = []
        for doc in documents:
            context_parts.append(f"Document: {doc.get('content', '')}")
        return "\n---\n".join(context_parts)

    @staticmethod
    def _calculate_confidence(documents: List[dict]) -> float:
        """Calculate confidence score"""
        if not documents:
            return 0.0
        
        scores = [doc.get('score', 0) for doc in documents]
        return sum(scores) / len(scores)
