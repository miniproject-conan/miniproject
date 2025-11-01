from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pytz import timezone

from app.core.security import get_current_user
from app.models.user import User
from app.repositories.diary_repo import (
    create_diary,
    delete_diary,
    get_diaries,
    get_diary,
    update_diary,
)
from app.repositories.question_repo import get_random_question_from_db
from app.schemas.diary import DiaryCreate, DiaryResponse, DiaryUpdate

router = APIRouter(tags=["Diary"])
templates = Jinja2Templates(directory="app/templates")


# HTML 렌더링 추가 -----------------------
# 일기 상세 페이지
@router.get("/read/{diary_id}", response_class=HTMLResponse)
async def render_diary_detail(
    request: Request, diary_id: int, current_user: User = Depends(get_current_user)
):
    post = await get_diary(diary_id, current_user)
    if not post:
        raise HTTPException(status_code=404, detail="해당 일기를 찾을 수 없습니다.")

    now = datetime.now(timezone("Asia/Seoul"))
    selected_year = now.year

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "post": post,
            "username": current_user.username,
            "selected_year": selected_year,
        },
    )


# 일기 월별 리스트
@router.get("/month", name="render_diary_list", response_class=HTMLResponse)
async def render_diary_list(
    request: Request,
    current_user: User = Depends(get_current_user),
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2000),
):
    posts = await get_diaries(current_user, month=month, year=year)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "username": current_user.username,
            "posts": posts,
            "user": current_user,
            "selected_year": year or datetime.now().year,
        },
    )


# -----------------------------------


# 전체 일기 조회
@router.get("", response_model=List[DiaryResponse], name="list_diaries")
async def get_all_diaries(current_user: User = Depends(get_current_user)):
    posts = await get_diaries(current_user)
    return posts


# 일기작성 (로드)
@router.get("/write")
async def render_write(request: Request, current_user=Depends(get_current_user)):
    questions = await get_random_question_from_db()
    return templates.TemplateResponse(
        "write.html",
        {
            "request": request,
            "user": current_user,
            "questions": questions,
            "post": None,
        },
    )


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


@router.get("/edit/{diary_id}", response_class=HTMLResponse)
async def render_edit_page(
    request: Request, diary_id: int, current_user: User = Depends(get_current_user)
):
    post = await get_diary(diary_id, current_user)
    if not post:
        raise HTTPException(status_code=404, detail="일기를 찾을 수 없습니다.")

    # 디버깅용
    # print("post.id:", post.id)
    # print("post.question:", post.question.content if post.question else None)

    return templates.TemplateResponse(
        "write.html", {"request": request, "user": current_user, "post": post}
    )


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
