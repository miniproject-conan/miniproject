from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(500), nullable=False)
