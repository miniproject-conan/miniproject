from tortoise import Tortoise

async def init_db(db_url: str):
    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["app.models.bookmark", "app.models.quote", "app.models.diary", "app.models.question", "app.models.user"]}  # 나중에 모델 추가 예정
    )
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()
