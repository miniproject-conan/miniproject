import json
from tortoise import Tortoise, run_async
from app.models.quote import Quote
from app.core.config import settings


async def init():
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models.quote"]},
    )
    await Tortoise.generate_schemas()


async def load_quotes_from_json(file_path: str):
    with open(file_path, "r", encoding="utf-8-sig") as f:
        quotes = json.load(f)

    inserted, skipped = 0, 0

    for q in quotes:
        quote, created = await Quote.get_or_create(
            author=q["author"].strip(),
            author_profile=q.get("authorProfile", "").strip(),
            message=q["message"].strip()
        )

        if created:
            inserted += 1
        else:
            skipped += 1

    print(f"[success] {len(quotes)} quotes inserted or verified.")


async def main():
    await init()
    await load_quotes_from_json("app/scraping/quotes.json")
    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(main())
