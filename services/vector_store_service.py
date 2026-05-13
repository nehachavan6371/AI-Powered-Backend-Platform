"""Vector Store Service - FAISS Integration"""

import logging
import os
from typing import List, Optional
import faiss
import numpy as np

from app.config import get_settings
from services.llm_service import LLMService

logger = logging.getLogger(__name__)
settings = get_settings()


class VectorStoreService:
    """Vector Store Service using FAISS"""

    def __init__(self):
        """Initialize vector store service"""
        self.llm_service = LLMService()
        self.index_path = settings.faiss_index_path
        self.dimension = settings.vector_dimension
        self.index = self._load_or_create_index()
        self.documents = {}  # In-memory document storage

    def _load_or_create_index(self) -> faiss.IndexFlatL2:
        """Load existing index or create new one"""
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        
        if os.path.exists(self.index_path):
            logger.info(f"Loading FAISS index from {self.index_path}")
            return faiss.read_index(self.index_path)
        else:
            logger.info(f"Creating new FAISS index")
            index = faiss.IndexFlatL2(self.dimension)
            return index

    async def add_document(self, doc_id: str, content: str, metadata: Optional[dict] = None) -> bool:
        """Add document to vector store"""
        try:
            # Generate embedding
            embedding = await self.llm_service.generate_embedding(content)
            embedding_array = np.array([embedding]).astype('float32')
            
            # Add to FAISS index
            self.index.add(embedding_array)
            
            # Store metadata
            self.documents[doc_id] = {
                "content": content,
                "metadata": metadata or {},
                "embedding": embedding
            }
            
            # Save index
            self._save_index()
            
            logger.info(f"Document {doc_id} added to vector store")
            return True
        
        except Exception as exc:
            logger.error(f"Error adding document: {exc}")
            return False

    async def search(self, query: str, top_k: int = 5) -> List[dict]:
        """Search for similar documents"""
        try:
            # Generate query embedding
            query_embedding = await self.llm_service.generate_embedding(query)
            query_array = np.array([query_embedding]).astype('float32')
            
            # Search in FAISS index
            distances, indices = self.index.search(query_array, top_k)
            
            # Retrieve documents
            results = []
            doc_list = list(self.documents.items())
            
            for idx, distance in zip(indices[0], distances[0]):
                if idx < len(doc_list):
                    doc_id, doc_data = doc_list[idx]
                    # Convert distance to similarity score (0-1)
                    similarity = 1 / (1 + distance)
                    results.append({
                        "document_id": doc_id,
                        "content": doc_data["content"],
                        "metadata": doc_data["metadata"],
                        "score": similarity
                    })
            
            return results
        
        except Exception as exc:
            logger.error(f"Error searching documents: {exc}")
            return []

    def _save_index(self):
        """Save FAISS index to disk"""
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)

    async def delete_document(self, doc_id: str) -> bool:
        """Delete document from vector store"""
        if doc_id in self.documents:
            del self.documents[doc_id]
            logger.info(f"Document {doc_id} deleted from vector store")
            return True
        return False

    async def rebuild_index(self) -> bool:
        """Rebuild FAISS index from documents"""
        try:
            logger.info("Rebuilding FAISS index")
            
            # Create new index
            embeddings = []
            for doc_data in self.documents.values():
                embeddings.append(doc_data["embedding"])
            
            if embeddings:
                embeddings_array = np.array(embeddings).astype('float32')
                self.index = faiss.IndexFlatL2(self.dimension)
                self.index.add(embeddings_array)
                self._save_index()
            
            logger.info("FAISS index rebuilt successfully")
            return True
        
        except Exception as exc:
            logger.error(f"Error rebuilding index: {exc}")
            return False
