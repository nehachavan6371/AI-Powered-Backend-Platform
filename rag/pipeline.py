"""RAG Pipeline Implementation"""

import logging
from typing import List, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class RAGPipeline:
    """RAG Pipeline for document processing and retrieval"""

    def __init__(self):
        """Initialize RAG pipeline"""
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.rag_chunk_size,
            chunk_overlap=settings.rag_chunk_overlap
        )

    def chunk_document(self, content: str) -> List[str]:
        """Split document into chunks"""
        try:
            chunks = self.splitter.split_text(content)
            logger.info(f"Document split into {len(chunks)} chunks")
            return chunks
        except Exception as exc:
            logger.error(f"Error chunking document: {exc}")
            return []

    def preprocess_document(self, content: str) -> str:
        """Preprocess document"""
        # Remove extra whitespace
        content = ' '.join(content.split())
        # Clean special characters
        content = content.encode('utf-8', errors='ignore').decode('utf-8')
        return content

    def rank_documents(self, documents: List[dict], scores: List[float]) -> List[Tuple[dict, float]]:
        """Rank documents by score"""
        ranked = list(zip(documents, scores))
        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked
