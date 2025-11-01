from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.security import get_current_user
from app.models.user import User
from app.repositories.diary_repo import (
    create_diary,
    delete_diary,
    get_diaries,
    get_diary,
    update_diary,
)
from app.schemas.diary import DiaryCreate, DiaryResponse, DiaryUpdate

router = APIRouter(prefix="/diary", tags=["Diary"])


# -----------------------------------


# 전체 일기 조회
@router.get("/", response_model=List[DiaryResponse], name="list_diaries")
async def get_all_diaries(current_user: User = Depends(get_current_user)):
    posts = await get_diaries(current_user)
    return posts


# 일기 작성 (진짜 작성)
@router.post("/write", name="create_diary", response_model=DiaryResponse)
async def create_diary_endpoint(
    diary: DiaryCreate,
    current_user: User = Depends(get_current_user),
):
    post = await create_diary(
        current_user,
        diary.title,
        diary.content,
        diary.question_id,
        diary.question_answer,
    )
    return post


# 일기 목록 조회 (월별)
@router.get("/list", name="list_monthly_diaries", response_model=List[DiaryResponse])
async def get_monthly_diaries(
    current_user: User = Depends(get_current_user),
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2000),
):
    posts = await get_diaries(current_user, month=month, year=year)
    return posts


# 특정 일기 조회
@router.get("/{diary_id}", response_model=DiaryResponse)
async def get_diary_endpoint(
    diary_id: int, current_user: User = Depends(get_current_user)
):
    post = await get_diary(diary_id, current_user)
    if not post:
        raise HTTPException(status_code=404, detail="해당 일기를 찾을 수 없습니다.")
    return post


# 일기 수정
@router.put("/{diary_id}", response_model=DiaryResponse)
async def update_diary_endpoint(
    diary_id: int, diary: DiaryUpdate, current_user: User = Depends(get_current_user)
):
    post = await get_diary(diary_id, current_user)
    if not post:
        raise HTTPException(status_code=404, detail="해당 일기를 찾을 수 없습니다.")
    post = await update_diary(post, diary.title, diary.content, diary.question_answer)
    return post


# 일기 삭제
@router.delete("/{diary_id}")
async def delete_diary_endpoint(
    diary_id: int, current_user: User = Depends(get_current_user)
):
    post = await get_diary(diary_id, current_user)
    if not post:
        raise HTTPException(status_code=404, detail="해당 일기를 찾을 수 없습니다.")
    await delete_diary(post, current_user)
    return {"message": "deleted"}
