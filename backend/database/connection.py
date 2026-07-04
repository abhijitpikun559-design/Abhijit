"""
Database connection and initialization
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

# Get database URL
DB_USER = os.getenv("DB_USER", "edugen_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "edugen_password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "edugen_db")

# PostgreSQL async connection string
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("DEBUG", "False") == "True",
    future=True,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=0
)

# Create session factory
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    """Dependency for getting database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    """Initialize database and create tables"""
    try:
        async with engine.begin() as conn:
            # Import all models to register them
            from database.models import Base
            
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Database tables created successfully")
    except Exception as e:
        print(f"⚠️  Database initialization error: {e}")

async def close_db():
    """Close database connection"""
    try:
        await engine.dispose()
        print("✅ Database connection closed")
    except Exception as e:
        print(f"⚠️  Error closing database: {e}")
