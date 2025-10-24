import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = "https://quotes-site-xi.vercel.app/"
driver.get(url)

time.sleep(2)

soup = BeautifulSoup(driver.page_source, "html.parser")

quotes = []
for card in soup.select("div.quote"):
    message = card.select_one("p.message")
    author = card.select_one("p.author")
    profile = card.select_one("p.profile")

    if message and author:
        quotes.append(
            {
                "author": author.get_text(strip=True).replace("-", "").strip(),
                "authorProfile": profile.get_text(strip=True) if profile else "",
                "message": message.get_text(strip=True).strip('"'),
            }
        )

driver.quit()

output_path = "quotes.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(quotes, f, ensure_ascii=False, indent=2)

print("\n명언 리스트\n" + "-" * 40)
for q in quotes:
    print(f"{q['author']} ({q['authorProfile']})")
    print(f"→ {q['message']}\n")

print("-" * 40)
print(f"완료! '{output_path}' 파일로 저장되었습니다.")
