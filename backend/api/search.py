"""
Search routes - Global search across platform
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from typing import Optional

from database.connection import get_db
from database.models import Document, Flashcard

router = APIRouter()

@router.get("/global")
async def global_search(
    user_id: str = Query(...),
    query: str = Query(..., min_length=2),
    search_type: str = Query("all", regex="^(all|documents|flashcards|quizzes)$"),
    db: AsyncSession = Depends(get_db)
):
    """
    Global search across all user content
    
    - **query**: Search query
    - **search_type**: Type of content to search (all/documents/flashcards/quizzes)
    """
    results = {}
    
    if search_type in ["all", "documents"]:
        # Search documents
        stmt = select(Document).where(
            (Document.owner_id == user_id) &
            or_(
                Document.title.ilike(f"%{query}%"),
                Document.description.ilike(f"%{query}%")
            )
        ).limit(10)
        result = await db.execute(stmt)
        results["documents"] = result.scalars().all()
    
    if search_type in ["all", "flashcards"]:
        # Search flashcards
        stmt = select(Flashcard).where(
            (Flashcard.user_id == user_id) &
            or_(
                Flashcard.question.ilike(f"%{query}%"),
                Flashcard.answer.ilike(f"%{query}%")
            )
        ).limit(10)
        result = await db.execute(stmt)
        results["flashcards"] = result.scalars().all()
    
    return {
        "query": query,
        "search_type": search_type,
        "results": results,
        "total": sum(len(v) if isinstance(v, list) else 0 for v in results.values())
    }

@router.get("/documents")
async def search_documents(
    user_id: str = Query(...),
    query: str = Query(..., min_length=2),
    db: AsyncSession = Depends(get_db)
):
    """
    Search in documents
    """
    stmt = select(Document).where(
        (Document.owner_id == user_id) &
        or_(
            Document.title.ilike(f"%{query}%"),
            Document.description.ilike(f"%{query}%")
        )
    ).limit(20)
    
    result = await db.execute(stmt)
    documents = result.scalars().all()
    
    return {"documents": documents, "total": len(documents)}

@router.get("/flashcards")
async def search_flashcards(
    user_id: str = Query(...),
    query: str = Query(..., min_length=2),
    db: AsyncSession = Depends(get_db)
):
    """
    Search in flashcards
    """
    stmt = select(Flashcard).where(
        (Flashcard.user_id == user_id) &
        or_(
            Flashcard.question.ilike(f"%{query}%"),
            Flashcard.answer.ilike(f"%{query}%")
        )
    ).limit(20)
    
    result = await db.execute(stmt)
    flashcards = result.scalars().all()
    
    return {"flashcards": flashcards, "total": len(flashcards)}

@router.get("/quiz-history")
async def search_quizzes(
    user_id: str = Query(...),
    query: str = Query(..., min_length=2),
    db: AsyncSession = Depends(get_db)
):
    """
    Search in quiz history
    """
    # TODO: Implement quiz search
    return {"quizzes": [], "total": 0}
