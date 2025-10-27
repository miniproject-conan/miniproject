from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

# 요청용 모델 (Create)
class DiaryCreate(BaseModel):
    title: str = Field(..., max_length=100)
    content: str

# 요청용 모델 (Update)
class DiaryUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    content: Optional[str]

# 응답용 모델
class DiaryResponse(BaseModel):
    id: int
    title: str
    content: str
    date: datetime  # 작성/수정 시간
    created_at: datetime

    class Config:
        orm_mode = True  # Tortoise ORM 객체 직렬화 허용
