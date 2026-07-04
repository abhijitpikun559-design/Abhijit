"""
Document management routes - Upload, list, delete documents
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
import os
import aiofiles
import uuid
from datetime import datetime

from database.connection import get_db
from database.models import Document, User

router = APIRouter()

# Pydantic models
class DocumentCreate(BaseModel):
    """Document creation schema"""
    title: str
    subject_id: str
    description: str = None
    semester: str = None
    topic: str = None

class DocumentResponse(BaseModel):
    """Document response schema"""
    id: str
    title: str
    description: str = None
    file_type: str
    file_size: int
    total_pages: int = None
    semester: str = None
    topic: str = None
    is_processed: bool
    created_at: str
    
    class Config:
        from_attributes = True

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    subject_id: str = Form(...),
    title: str = Form(...),
    description: str = Form(None),
    semester: str = Form(None),
    topic: str = Form(None),
    user_id: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a study material document
    
    Supported formats: PDF, DOCX, PPTX, TXT
    Max file size: 50MB
    """
    # Validate file type
    allowed_extensions = {".pdf", ".docx", ".pptx", ".txt"}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file_ext} not allowed. Allowed: {allowed_extensions}"
        )
    
    # Validate file size (50MB)
    max_size = int(os.getenv("MAX_UPLOAD_SIZE", "52428800"))
    file_content = await file.read()
    file_size = len(file_content)
    
    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size {file_size} exceeds maximum {max_size} bytes"
        )
    
    # Check user exists
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create upload directory
    upload_dir = os.getenv("UPLOAD_DIR", "./uploads")
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Save file
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(file_content)
    
    # Create document record
    document = Document(
        owner_id=user_id,
        subject_id=subject_id,
        title=title,
        description=description,
        file_path=unique_filename,
        file_type=file_ext.lstrip("."),
        file_size=file_size,
        semester=semester,
        topic=topic,
        is_processed=False
    )
    
    db.add(document)
    await db.commit()
    await db.refresh(document)
    
    return document

@router.get("/")
async def list_documents(
    user_id: str,
    subject_id: str = None,
    db: AsyncSession = Depends(get_db)
):
    """
    List all documents for a user
    
    - **user_id**: User ID (required)
    - **subject_id**: Filter by subject (optional)
    """
    query = select(Document).where(Document.owner_id == user_id)
    
    if subject_id:
        query = query.where(Document.subject_id == subject_id)
    
    query = query.order_by(Document.created_at.desc())
    result = await db.execute(query)
    documents = result.scalars().all()
    
    return {"documents": documents, "total": len(documents)}

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific document
    """
    stmt = select(Document).where(Document.id == document_id)
    result = await db.execute(stmt)
    document = result.scalars().first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return document

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: str,
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a document
    """
    stmt = select(Document).where(
        (Document.id == document_id) & (Document.owner_id == user_id)
    )
    result = await db.execute(stmt)
    document = result.scalars().first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Delete file
    upload_dir = os.getenv("UPLOAD_DIR", "./uploads")
    file_path = os.path.join(upload_dir, document.file_path)
    
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Delete database record
    await db.delete(document)
    await db.commit()
    
    return None

@router.put("/{document_id}")
async def update_document(
    document_id: str,
    user_id: str,
    title: str = None,
    description: str = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Update document metadata
    """
    stmt = select(Document).where(
        (Document.id == document_id) & (Document.owner_id == user_id)
    )
    result = await db.execute(stmt)
    document = result.scalars().first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    if title:
        document.title = title
    if description is not None:
        document.description = description
    
    document.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(document)
    
    return document
