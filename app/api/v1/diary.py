from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryResponse
from app.repositories.diary_repo import create_diary, get_diary, get_diaries, update_diary, delete_diary
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter( tags=["Diary"])

# 일기 작성
@router.post("/", response_model=DiaryResponse)
async def create_diary_endpoint(diary: DiaryCreate, current_user: User = Depends(get_current_user)):
    post = await create_diary(current_user, diary.title, diary.content)
    return post

# 일기 목록 조회 (월별/주별)
@router.get("/", response_model=List[DiaryResponse])
async def get_diaries_endpoint(
    current_user: User = Depends(get_current_user),
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2000),
    week: Optional[int] = Query(None, ge=1, le=53)
):
    posts = await get_diaries(current_user, month=month, year=year, week=week)
    return posts

# 특정 일기 조회
@router.get("/{diary_id}", response_model=DiaryResponse)
async def get_diary_endpoint(diary_id: int, current_user: User = Depends(get_current_user)):
    post = await get_diary(diary_id, current_user)
    if not post:
        raise HTTPException(status_code=404, detail="해당 일기를 찾을 수 없습니다.")
    return post

# 일기 수정
@router.put("/{diary_id}", response_model=DiaryResponse)
async def update_diary_endpoint(diary_id: int, diary: DiaryUpdate, current_user: User = Depends(get_current_user)):
    post = await get_diary(diary_id, current_user)
    if not post:
        raise HTTPException(status_code=404, detail="해당 일기를 찾을 수 없습니다.")
    post = await update_diary(post, diary.title, diary.content)
    return post

# 일기 삭제
@router.delete("/{diary_id}")
async def delete_diary_endpoint(diary_id: int, current_user: User = Depends(get_current_user)):
    post = await get_diary(diary_id, current_user)
    if not post:
        raise HTTPException(status_code=404, detail="해당 일기를 찾을 수 없습니다.")
    await delete_diary(post, current_user)
    return {"message": "deleted"}
