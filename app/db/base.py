from sqlalchemy.orm import declarative_base
from app.models.user import User
from app.models.diary import Post

Base = declarative_base()

__all__ = ["User", "Post"]      # ORM에서 모든 파일 한번에 불러오기