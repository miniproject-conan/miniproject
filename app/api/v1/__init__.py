# API 버전별 라우터 묶음
from fastapi import APIRouter

from app.api.v1 import auth, bookmark, diary, question, quote

router = APIRouter()
router.include_router(auth.router)
router.include_router(diary.router)
router.include_router(quote.router)
router.include_router(bookmark.router)
router.include_router(question.router)
