from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pytz import timezone

from app.core.security import get_current_user
from app.models.user import User
from app.repositories.diary_repo import get_diaries, get_diary
from app.repositories.question_repo import get_random_question_from_db

html_router = APIRouter(prefix="/diary", tags=["Diary"])
templates = Jinja2Templates(directory="app/templates")


# HTML 렌더링 추가 -----------------------
# 일기 상세 페이지
@html_router.get("/read/{diary_id}", response_class=HTMLResponse)
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
@html_router.get("/month", name="render_diary_list", response_class=HTMLResponse)
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


# 일기 수정
@html_router.get("/edit/{diary_id}", response_class=HTMLResponse)
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


# 일기작성 (로드)
@html_router.get("/write")
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
