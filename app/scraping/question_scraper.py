import asyncio
import time
from copy import deepcopy

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from tortoise import Tortoise
from webdriver_manager.chrome import ChromeDriverManager

from app.db.config import TORTOISE_ORM
from app.models.questions import Questions

# import os, sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


async def scrape_questions():

    # db 초기화 먼저
    orm_config = deepcopy(TORTOISE_ORM)
    orm_config["apps"]["models"]["models"] = ["app.models.questions"]

    await Tortoise.init(config=orm_config)
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

    questions = [
        li.get_text(strip=True)
        for li in soup.select(".question-text")
        if li.get_text(strip=True)
    ]

    inserted, skipped = 0, 0
    for text in questions:
        _, created = await Questions.get_or_create(content=text)
        if created:
            inserted += 1
        else:
            skipped += 1

    print(f"Inserted {inserted} questions")

    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(scrape_questions())

# 1. 외부 사이트에서 질문 긁어와서 DB에 저장하는 코드
