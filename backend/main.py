"""
EduGen AI - Main FastAPI Application

This module initializes the FastAPI application and sets up all routes and middleware.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv()

# Import routes
try:
    from api.auth import router as auth_router
    from api.documents import router as documents_router
    from api.ai_assistant import router as ai_router
    from api.quiz import router as quiz_router
    from api.flashcards import router as flashcards_router
    from api.planner import router as planner_router
    from api.analytics import router as analytics_router
    from api.search import router as search_router
    from api.profile import router as profile_router
except ImportError as e:
    print(f"⚠️  Warning: Could not import some routers: {e}")

# Import database setup
try:
    from database.connection import init_db, close_db
except ImportError as e:
    print(f"⚠️  Warning: Could not import database: {e}")
    async def init_db():
        print("Database initialization skipped")
    async def close_db():
        print("Database cleanup skipped")

# Lifespan context
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting EduGen AI Backend...")
    try:
        await init_db()
    except Exception as e:
        print(f"⚠️  Database initialization error: {e}")
    yield
    # Shutdown
    print("🛑 Shutting down EduGen AI Backend...")
    try:
        await close_db()
    except Exception as e:
        print(f"⚠️  Database cleanup error: {e}")

# Initialize FastAPI app
app = FastAPI(
    title="EduGen AI - Intelligent Study Assistant",
    description="API for AI-powered study platform",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
upload_dir = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(upload_dir, exist_ok=True)

# Mount static files for uploads
try:
    app.mount(
        "/uploads",
        StaticFiles(directory=upload_dir),
        name="uploads"
    )
except Exception as e:
    print(f"⚠️  Could not mount uploads: {e}")

# Health check endpoint
@app.get("/api/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "EduGen AI Backend",
        "version": "1.0.0"
    }

# Include routers
try:
    app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(documents_router, prefix="/api/documents", tags=["Documents"])
    app.include_router(ai_router, prefix="/api/ai", tags=["AI Assistant"])
    app.include_router(quiz_router, prefix="/api/quiz", tags=["Quiz"])
    app.include_router(flashcards_router, prefix="/api/flashcards", tags=["Flashcards"])
    app.include_router(planner_router, prefix="/api/planner", tags=["Study Planner"])
    app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])
    app.include_router(search_router, prefix="/api/search", tags=["Search"])
    app.include_router(profile_router, prefix="/api/profile", tags=["Profile"])
except Exception as e:
    print(f"⚠️  Could not include routers: {e}")

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to EduGen AI - Intelligent Study Assistant",
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("SERVER_PORT", "8000")),
        reload=os.getenv("DEBUG", "False") == "True"
    )
