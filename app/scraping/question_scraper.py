import httpx
from bs4 import BeautifulSoup
from app.models.question import Question
from app.db.session import get_session

async def scrape_question():
    url = "https://my-life-question.vercel.app/"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")

    question_texts = [q.get_text(strip=True) for q in soup.select("li") if q.get_text(strip=True)]

    async for session in get_session():
        for text in question_texts:
            session.add(Question(content=text))
        await session.commit()

# 1. 외부 사이트에서 질문 긁어와서 DB에 저장하는 코드