"""
User Profile routes - Profile management and settings
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from database.connection import get_db
from database.models import User

router = APIRouter()

class UserUpdate(BaseModel):
    """User update schema"""
    full_name: str = None
    bio: str = None
    avatar_url: str = None

class UserProfileResponse(BaseModel):
    """User profile response"""
    id: str
    username: str
    email: str
    full_name: str
    bio: str = None
    avatar_url: str = None
    created_at: str
    
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
