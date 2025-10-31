import random
from app.models.questions import Questions

#DB에서 무작위 1개
async def get_random_question_from_db():

    try:
        question = await Questions.all()
        # 질문 x
        if not question:
            print("question", question)
            return None

        # 무작위 1개
        question = random.choice(question)
        print(question)
        return question
    except Exception as e:
        print("왜? ", e)
        return None




#DB에서 가져오는거
async def get_all_questions_from_db():
    question = await Questions.all()
    return question



    
# 3. DB에서 무작위 1개를 질문을 선택해서 반환