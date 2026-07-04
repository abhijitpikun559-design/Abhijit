"""
SQLAlchemy ORM Models for EduGen AI
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, Table, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(120), nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    documents = relationship("Document", back_populates="owner")
    quiz_responses = relationship("QuizResponse", back_populates="user")
    study_sessions = relationship("StudySession", back_populates="user")
    progress = relationship("Progress", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

class Subject(Base):
    """Subject model"""
    __tablename__ = "subjects"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(120), nullable=False, index=True)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    documents = relationship("Document", back_populates="subject")
    progress = relationship("Progress", back_populates="subject")

class Document(Base):
    """Document model"""
    __tablename__ = "documents"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    subject_id = Column(String(36), ForeignKey("subjects.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String(255), nullable=False)
    file_type = Column(String(20), nullable=False)  # pdf, docx, pptx, txt
    file_size = Column(Integer, nullable=False)  # in bytes
    total_pages = Column(Integer, nullable=True)
    semester = Column(String(50), nullable=True)
    topic = Column(String(120), nullable=True)
    is_processed = Column(Boolean, default=False)
    chroma_collection_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="documents")
    subject = relationship("Subject", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")

class DocumentChunk(Base):
    """Document chunks for RAG"""
    __tablename__ = "document_chunks"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    page_number = Column(Integer, nullable=True)
    embedding_id = Column(String(255), nullable=True)  # Chroma embedding ID
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    document = relationship("Document", back_populates="chunks")

class Flashcard(Base):
    """Flashcard model"""
    __tablename__ = "flashcards"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    tags = Column(JSON, nullable=True)
    marked_known = Column(Boolean, default=False)
    marked_revision = Column(Boolean, default=False)
    review_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_reviewed_at = Column(DateTime, nullable=True)

class Quiz(Base):
    """Quiz model"""
    __tablename__ = "quiz"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    difficulty = Column(String(20), nullable=False)  # easy, medium, hard
    total_questions = Column(Integer, default=0)
    duration_minutes = Column(Integer, nullable=True)
    passing_score = Column(Float, default=60.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")
    responses = relationship("QuizResponse", back_populates="quiz", cascade="all, delete-orphan")

class QuizQuestion(Base):
    """Quiz question model"""
    __tablename__ = "quiz_questions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    quiz_id = Column(String(36), ForeignKey("quiz.id"), nullable=False, index=True)
    question_type = Column(String(20), nullable=False)  # mcq, true_false, short, long
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=True)  # For MCQ
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    quiz = relationship("Quiz", back_populates="questions")
    responses = relationship("QuizResponse", back_populates="question", cascade="all, delete-orphan")

class QuizResponse(Base):
    """User quiz responses"""
    __tablename__ = "quiz_responses"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    quiz_id = Column(String(36), ForeignKey("quiz.id"), nullable=False, index=True)
    question_id = Column(String(36), ForeignKey("quiz_questions.id"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    user_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    time_spent_seconds = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    quiz = relationship("Quiz", back_populates="responses")
    question = relationship("QuizQuestion", back_populates="responses")
    user = relationship("User", back_populates="quiz_responses")

class Progress(Base):
    """Learning progress tracking"""
    __tablename__ = "progress"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    subject_id = Column(String(36), ForeignKey("subjects.id"), nullable=False, index=True)
    total_documents = Column(Integer, default=0)
    completed_quizzes = Column(Integer, default=0)
    average_quiz_score = Column(Float, default=0.0)
    study_hours = Column(Float, default=0.0)
    study_streak = Column(Integer, default=0)
    last_studied = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="progress")
    subject = relationship("Subject", back_populates="progress")

class StudySession(Base):
    """Study session logs"""
    __tablename__ = "study_sessions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=True)
    session_type = Column(String(50), nullable=False)  # reading, quiz, flashcard, planning
    duration_minutes = Column(Integer, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="study_sessions")

class Notification(Base):
    """User notifications"""
    __tablename__ = "notifications"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)  # exam_reminder, goal_reminder, etc
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="notifications")
