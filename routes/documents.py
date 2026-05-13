"""Document Routes"""

import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, status

from models.schemas import DocumentUploadResponse, DocumentListResponse
from app.dependencies import VectorStoreServiceDep

router = APIRouter()


@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    vector_store: VectorStoreServiceDep = None
):
    """Upload document"""
    try:
        doc_id = str(uuid.uuid4())
        content = await file.read()
        
        # Add to vector store
        success = await vector_store.add_document(
            doc_id,
            content.decode('utf-8'),
            metadata={"filename": file.filename, "content_type": file.content_type}
        )
        
        if success:
            return DocumentUploadResponse(
                document_id=doc_id,
                filename=file.filename,
                size=len(content),
                status="uploaded"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload document"
            )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )


@router.get("/documents", response_model=DocumentListResponse)
async def list_documents(skip: int = 0, limit: int = 10):
    """List documents"""
    return DocumentListResponse(
        total=0,
        documents=[]
    )


@router.delete("/documents/{document_id}")
async def delete_document(document_id: str, vector_store: VectorStoreServiceDep = None):
    """Delete document"""
    success = await vector_store.delete_document(document_id)
    if success:
        return {"status": "deleted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )


@router.post("/documents/index")
async def rebuild_index(vector_store: VectorStoreServiceDep = None):
    """Rebuild vector index"""
    success = await vector_store.rebuild_index()
    if success:
        return {"status": "index_rebuilt"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to rebuild index"
        )
