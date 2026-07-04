"""
Quiz routes - Generate, manage, and attempt quizzes
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from database.connection import get_db
from database.models import Document, Quiz

router = APIRouter()

class QuizGenerateRequest(BaseModel):
    """Quiz generation request"""
    document_id: str
    difficulty: str = "medium"  # easy, medium, hard
    num_questions: int = 10
    question_types: List[str] = ["mcq", "true_false", "short"]

class QuizQuestion(BaseModel):
    """Quiz question schema"""
    id: str
    question_text: str
    question_type: str
    options: Optional[List[str]] = None
    order: int

class QuizResponse(BaseModel):
    """Quiz response"""
    id: str
    title: str
    total_questions: int
    difficulty: str
    duration_minutes: Optional[int] = None

class QuizSubmission(BaseModel):
    """Quiz submission schema"""
    quiz_id: str
    responses: Dict[str, str]  # question_id: user_answer
    user_id: str

class QuizResult(BaseModel):
    """Quiz result schema"""
    score: float
    total: int
    percentage: float
    passed: bool
    detailed_results: List[Dict[str, Any]] = []

@router.post("/generate", response_model=QuizResponse)
async def generate_quiz(
    request: QuizGenerateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate a quiz from a document
    
    - **document_id**: Source document
    - **difficulty**: Quiz difficulty level
    - **num_questions**: Number of questions
    - **question_types**: Types of questions to include
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
    
    # TODO: Implement quiz generation with LLM
    return QuizResponse(
        id="quiz123",
        title=f"Auto-generated Quiz from {document.title}",
        total_questions=request.num_questions,
        difficulty=request.difficulty
    )

@router.get("/{quiz_id}")
async def get_quiz(
    quiz_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a quiz with all questions
    """
    stmt = select(Quiz).where(Quiz.id == quiz_id)
    result = await db.execute(stmt)
    quiz = result.scalars().first()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    return {
        "quiz_id": quiz.id,
        "title": quiz.title,
        "total_questions": quiz.total_questions,
        "difficulty": quiz.difficulty,
        "duration_minutes": quiz.duration_minutes,
        "questions": []
    }

@router.post("/{quiz_id}/submit", response_model=QuizResult)
async def submit_quiz(
    quiz_id: str,
    submission: QuizSubmission,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit quiz responses and get score
    
    - **quiz_id**: Quiz ID
    - **responses**: User's answers {question_id: answer}
    - **user_id**: User ID
    """
    # Verify quiz exists
    stmt = select(Quiz).where(Quiz.id == quiz_id)
    result = await db.execute(stmt)
    quiz = result.scalars().first()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    # TODO: Calculate score and store responses
    return QuizResult(
        score=0.0,
        total=quiz.total_questions,
        percentage=0.0,
        passed=False,
        detailed_results=[]
    )

@router.get("/history/{user_id}")
async def get_quiz_history(
    user_id: str,
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user's quiz history
    """
    return {"quizzes": [], "total": 0}
