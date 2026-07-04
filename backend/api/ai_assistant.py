"""
AI Assistant routes - Question answering, summaries, explanations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, List

from database.connection import get_db
from database.models import Document
from sqlalchemy.future import select

router = APIRouter()

class QuestionRequest(BaseModel):
    """Question request schema"""
    document_id: str
    question: str
    mode: str = "intermediate"  # beginner, intermediate, advanced
    
    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "doc123",
                "question": "What is photosynthesis?",
                "mode": "intermediate"
            }
        }

class SourceReference(BaseModel):
    """Source reference schema"""
    page_number: Optional[int] = None
    snippet: str
    relevance_score: float = 0.0

class AnswerResponse(BaseModel):
    """Answer response schema"""
    answer: str
    sources: List[SourceReference] = []
    confidence: float = 0.0
    mode: str = "intermediate"

class SummaryRequest(BaseModel):
    """Summary request schema"""
    document_id: str
    summary_type: str = "chapter"  # chapter, bullet, key_points, exam

class ExplainRequest(BaseModel):
    """Explain request schema"""
    concept: str
    mode: str = "intermediate"  # beginner, intermediate, advanced
    context: Optional[str] = None

@router.post("/ask", response_model=AnswerResponse)
async def ask_question(
    request: QuestionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Ask a question about a document using RAG
    
    - **document_id**: Document to query
    - **question**: Your question
    - **mode**: Response complexity (beginner/intermediate/advanced)
    """
    # Verify document exists
    stmt = select(Document).where(Document.id == request.document_id)
    result = await db.execute(stmt)
    document = result.scalars().first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # TODO: Implement RAG pipeline with ChromaDB and LangChain
    # This endpoint will:
    # 1. Retrieve relevant chunks from ChromaDB
    # 2. Send to LLM with context
    # 3. Return answer with citations
    
    return AnswerResponse(
        answer="This endpoint will use RAG to answer questions about your documents. Implementation pending.",
        sources=[],
        confidence=0.0,
        mode=request.mode
    )

@router.post("/summarize")
async def summarize_document(
    request: SummaryRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate a summary of a document
    
    - **document_id**: Document to summarize
    - **summary_type**: Type of summary (chapter/bullet/key_points/exam)
    """
    # Verify document exists
    stmt = select(Document).where(Document.id == request.document_id)
    result = await db.execute(stmt)
    document = result.scalars().first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # TODO: Implement summarization with LLM
    return {
        "summary": f"Summary will be generated here for {request.summary_type} type",
        "summary_type": request.summary_type,
        "document_id": request.document_id
    }

@router.post("/explain")
async def explain_concept(
    request: ExplainRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Get an explanation of a concept
    
    - **concept**: Concept to explain
    - **mode**: Explanation level (beginner/intermediate/advanced)
    - **context**: Optional context document ID
    """
    # TODO: Implement concept explanation with LLM
    return {
        "explanation": f"Detailed {request.mode} level explanation will appear here",
        "mode": request.mode,
        "examples": [],
        "related_concepts": []
    }
