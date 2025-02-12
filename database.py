from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class SentimentRecord(Base):
    __tablename__ = "sentiment_records"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    sentiment = Column(String(10), nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create all tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_sentiment_analysis(text: str, sentiment: str, confidence: float):
    """Save sentiment analysis result to database"""
    db = next(get_db())
    try:
        # Convert numpy.float64 to Python float
        confidence_value = float(confidence)
        db_record = SentimentRecord(
            input_text=text,
            sentiment=sentiment,
            confidence=confidence_value
        )
        db.add(db_record)
        db.commit()
        return db_record
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def get_recent_analyses(limit: int = 5):
    """Get recent sentiment analyses"""
    db = next(get_db())
    try:
        return db.query(SentimentRecord)\
            .order_by(SentimentRecord.created_at.desc())\
            .limit(limit)\
            .all()
    finally:
        db.close()
