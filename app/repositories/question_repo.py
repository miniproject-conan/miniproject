import random
from app.models.question import Question

#DB에서 무작위 1개
async def get_random_question_from_db():
    #모든 질문
    question = await Question.all()

    #질문 x
    if not question:
        return None
    
    #무작위 1개
    question = random.choice(question)
    return question

#DB에서 가져오는거
async def get_all_questions_from_db():
    question = await Question.all()
    return question



    
# 3. DB에서 무작위 1개를 질문을 선택해서 반환