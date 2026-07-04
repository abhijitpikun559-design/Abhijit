"""
Flashcard routes - Create, manage, and review flashcards
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import Optional, List

from database.connection import get_db
from database.models import Flashcard, Document

router = APIRouter()

class FlashcardCreate(BaseModel):
    """Flashcard creation schema"""
    document_id: Optional[str] = None
    question: str
    answer: str
    difficulty: str = "medium"
    tags: List[str] = []

class FlashcardResponse(BaseModel):
    """Flashcard response schema"""
    id: str
    question: str
    answer: str
    difficulty: str
    marked_known: bool
    marked_revision: bool
    review_count: int = 0
    
    class Config:
        from_attributes = True

@router.post("/generate")
async def generate_flashcards(
    document_id: str = Query(...),
    user_id: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Auto-generate flashcards from a document
    """
    # Verify document exists
    stmt = select(Document).where(Document.id == document_id)
    result = await db.execute(stmt)
    document = result.scalars().first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # TODO: Implement flashcard generation with LLM
    return {
        "flashcards_created": 0,
        "document_id": document_id,
        "message": "Flashcard generation coming soon"
    }

@router.post("/", response_model=FlashcardResponse)
async def create_flashcard(
    flashcard: FlashcardCreate,
    user_id: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a manual flashcard
    """
    new_flashcard = Flashcard(
        user_id=user_id,
        document_id=flashcard.document_id,
        question=flashcard.question,
        answer=flashcard.answer,
        difficulty=flashcard.difficulty,
        tags=flashcard.tags if flashcard.tags else None
    )
    
    db.add(new_flashcard)
    await db.commit()
    await db.refresh(new_flashcard)
    
    return new_flashcard

@router.get("/user/{user_id}")
async def get_user_flashcards(
    user_id: str,
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all flashcards for a user
    """
    stmt = select(Flashcard).where(
        Flashcard.user_id == user_id
    ).order_by(Flashcard.created_at.desc()).limit(limit)
    
    result = await db.execute(stmt)
    flashcards = result.scalars().all()
    
    return {"flashcards": flashcards, "total": len(flashcards)}

@router.put("/{flashcard_id}/mark-known")
async def mark_known(
    flashcard_id: str,
    user_id: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Mark a flashcard as known
    """
    stmt = select(Flashcard).where(
        (Flashcard.id == flashcard_id) & (Flashcard.user_id == user_id)
    )
    result = await db.execute(stmt)
    flashcard = result.scalars().first()
    
    if not flashcard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard not found"
        )
    
    flashcard.marked_known = True
    flashcard.marked_revision = False
    flashcard.review_count += 1
    await db.commit()
    
    return {"message": "Flashcard marked as known"}

@router.put("/{flashcard_id}/mark-revision")
async def mark_revision(
    flashcard_id: str,
    user_id: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Mark a flashcard for revision
    """
    stmt = select(Flashcard).where(
        (Flashcard.id == flashcard_id) & (Flashcard.user_id == user_id)
    )
    result = await db.execute(stmt)
    flashcard = result.scalars().first()
    
    if not flashcard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard not found"
        )
    
    flashcard.marked_revision = True
    flashcard.marked_known = False
    await db.commit()
    
    return {"message": "Flashcard marked for revision"}

@router.delete("/{flashcard_id}")
async def delete_flashcard(
    flashcard_id: str,
    user_id: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a flashcard
    """
    stmt = select(Flashcard).where(
        (Flashcard.id == flashcard_id) & (Flashcard.user_id == user_id)
    )
    result = await db.execute(stmt)
    flashcard = result.scalars().first()
    
    if not flashcard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard not found"
        )
    
    await db.delete(flashcard)
    await db.commit()
    
    return {"message": "Flashcard deleted"}
