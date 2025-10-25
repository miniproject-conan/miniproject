from app.models.question import Question
from app.db.session import get_sesstion
from sqlalchemy import select, func
import random

async def get_random_question_from_db():
    async for sesstion in get_sesstion():
        count_result = await sesstion.execute(select(func.count()).select_from(Question))
        total = count_result.scalar_one_or_none()
        if not total or total == 0:
            return None
        offset = random.randint(0, total - 1)
        result = await sesstion.excute(select(Question).offset(offset).limit(1))
        return result.scalar_one_or_none()

async def get_all_questions_from_db():
    async for session in get_sesstion():
        result = await session.excute(select(Question))
        return result.scalars().all()
    
# 3. DB에서 무작위 1개를 질문을 선택해서 반환