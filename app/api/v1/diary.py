from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import date, datetime, timedelta
from pydantic import BaseModel, Field

from app.models.diary import Post
from app.models.user import User
from app.core.security import get_current_user
from tortoise.contrib.pydantic import pydantic_model_creator

router = APIRouter(prefix="/diary", tags=["diary"])


# Pydantic 모델
# 입력 검증용
class DiaryCreate(BaseModel):
    title: str = Field(..., max_length=100)
    content: str

class DiaryUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    content: Optional[str]


# 출력용
Diary_Pydantic = pydantic_model_creator(Post, name="Diary", exclude=("author",))
DiaryResponse = Diary_Pydantic


# CRUD API

# 1. 일기 작성
@router.post("/", response_model=DiaryResponse)
async def create_diary(diary: DiaryCreate, current_user: User = Depends(get_current_user)):
    object = await Post.create(
        title=diary.title,
        content=diary.content,
        date=date.today(),
        author=current_user
    )
    current_user.number_of_posts += 1
    await current_user.save()
    return await Diary_Pydantic.from_tortoise_orm(object)

# 2️. 일기 목록 조회 (월별/주별 정렬 가능)
@router.get("/", response_model=List[DiaryResponse])
async def get_diaries(
    current_user: User = Depends(get_current_user),
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2000),
    week: Optional[int] = Query(None, ge=1, le=53)
):
    query = Post.filter(author=current_user)

    # 월별 조회
    if year and month:
        query = query.filter(date__year=year, date__month=month)

    # 주별 조회
    elif year and week:
        first_day = date.fromisocalendar(year, week, 1)
        last_day = first_day + timedelta(days=6)
        query = query.filter(date__gte=first_day, date__lte=last_day)

    posts = await query.order_by("-date").all()
    return await Diary_Pydantic.from_queryset(posts)

# 3️. 특정 일기 조회
@router.get("/{diary_id}", response_model=DiaryResponse)
async def get_diary(diary_id: int, current_user: User = Depends(get_current_user)):
    post = await Post.filter(id=diary_id, author=current_user).first()
    if not post:
        raise HTTPException(status_code=404, detail="해당 일기를 찾을 수 없습니다.")
    return await Diary_Pydantic.from_tortoise_orm(post)

# 4️. 일기 수정
@router.put("/{diary_id}", response_model=DiaryResponse)
async def update_diary(diary_id: int, diary: DiaryUpdate, current_user: User = Depends(get_current_user)):
    post = await Post.filter(id=diary_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="해당 일기를 찾을 수 없습니다.")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="접근 권한이 없습니다.")
    if diary.title is not None:
        post.title = diary.title
    if diary.content is not None:
        post.content = diary.content
    post.date = date.today()  # 수정 날짜로 덮어쓰기
    await post.save()
    return await Diary_Pydantic.from_tortoise_orm(post)

# 5️. 일기 삭제
@router.delete("/{diary_id}")
async def delete_diary(diary_id: int, current_user: User = Depends(get_current_user)):
    post = await Post.filter(id=diary_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="해당 일기를 찾을 수 없습니다.")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="접근 권한이 없습니다.")
    await post.delete()
    current_user.number_of_posts = max(0, current_user.number_of_posts - 1)
    await current_user.save()
    return {"message": "deleted"}
