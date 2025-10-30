import asyncio
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from tortoise import Tortoise
from app.models.question import Question
from app.core.config import settings

async def scrape_questions():

    # db 초기화 먼저
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models.question"]},
    )
    await Tortoise.generate_schemas()

    # EC2용 headless Chrome 옵션 추가
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )

    url = "https://my-life-question.vercel.app/"
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    questions = [li.get_text(strip=True) for li in soup.select("li") if li.get_text(strip=True)]

    inserted, skipped = 0, 0
    for text in questions:
        _, created = await Question.get_or_create(content=text)
        if created:
            inserted += 1
        else:
            skipped += 1

    print(f"Inserted {inserted} questions")

    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(scrape_questions())

# 1. 외부 사이트에서 질문 긁어와서 DB에 저장하는 코드