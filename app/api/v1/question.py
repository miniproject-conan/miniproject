from fastapi import APIRouter, HTTPException
from app.services.question_service import get_random_question, get_all_question

from typing import List

router = APIRouter(tags=["Question"])

@router.get("/random")
async def get_random_self_reflection_question():
    question = await get_random_question()
    if not question:
        raise HTTPException(status_code=404, detail="질문이 존재 하지않음.")
    return {"question": question.content}


@router.get("/me", response_model=List[dict])
async def my_questions():
    qs = await get_all_question()
    return [{"id": q.id, "question_text": q.content} for q in qs]

# 4. 랜덤 자기성찰 질문을 1개 반환함.
