from fastapi import APIRouter

from app.views import auth, diary

html_router = APIRouter()
html_router.include_router(auth.html_router)
html_router.include_router(diary.html_router)
