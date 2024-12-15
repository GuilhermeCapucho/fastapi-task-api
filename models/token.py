from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class ActiveToken(Base):
    __tablename__ = "active_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)