from typing import List

from fastapi import APIRouter

from app.models.question import Question

router = APIRouter(prefix="/question", tags=["question"])


@router.get("/random")
async def random_question():
    q = await Question.first()
    if not q:
        return {"id": 0, "question_text": "샘플 질문이 없습니다."}
    return {"id": q.id, "question_text": q.question_text}


@router.get("/me", response_model=List[dict])
async def my_questions():
    qs = await Question.all()
    return [{"id": q.id, "question_text": q.question_text} for q in qs]
