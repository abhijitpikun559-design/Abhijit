"""
User Profile routes - Profile management and settings
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from database.connection import get_db
from database.models import User

router = APIRouter()

class UserUpdate(BaseModel):
    """User update schema"""
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserProfileResponse(BaseModel):
    """User profile response"""
    id: str
    username: str
    email: str
    full_name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: str
    is_active: bool
    
    class Config:
        from_attributes = True

@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get user profile
    """
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.put("/{user_id}", response_model=UserProfileResponse)
async def update_user_profile(
    user_id: str,
    update_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update user profile
    """
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if update_data.full_name:
        user.full_name = update_data.full_name
    if update_data.bio is not None:
        user.bio = update_data.bio
    if update_data.avatar_url:
        user.avatar_url = update_data.avatar_url
    
    user.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(user)
    
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete user account
    """
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    await db.delete(user)
    await db.commit()
    
    return None

@router.get("/statistics/{user_id}")
async def get_user_statistics(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get user statistics
    """
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # TODO: Calculate user statistics
    return {
        "user_id": user_id,
        "total_documents": 0,
        "total_flashcards": 0,
        "total_quizzes_taken": 0,
        "total_study_hours": 0.0
    }
