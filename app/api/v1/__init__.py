# API 버전별 라우터 묶음
from fastapi import APIRouter
from app.api.v1 import auth, diary, quote, bookmark, question

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(diary.router, prefix="/diary", tags=["Diary"])
router.include_router(quote.router, prefix="/quote", tags=["Quote"])
router.include_router(bookmark.router, prefix="/bookmark", tags=["Bookmark"])
router.include_router(question.router, prefix="/question", tags=["Question"])
