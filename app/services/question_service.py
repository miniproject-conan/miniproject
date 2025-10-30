from app.repositories.question_repo import get_random_question_from_db, get_all_questions_from_db

async def get_random_question():
    return await get_random_question_from_db()

async def get_all_question():
    return await get_all_questions_from_db()

# 2. 유저가 랜덤 질문 요청함.