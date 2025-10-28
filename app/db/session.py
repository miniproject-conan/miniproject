from tortoise import Tortoise
from app.core.config import settings


async def init_db() -> None:
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models"]}
    )
    await Tortoise.generate_schemas()
    print("✅ Database initialized successfully")


async def close_db() -> None:
    await Tortoise.close_connections()
    print("🛑 Database connections closed")



# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
#
# from app.core.config import settings
#
# engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)
# async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
#
#
# async def get_db():
#     async with async_session() as session:
#         yield session
#
#
# async def init_db():
#     from app.db.base import Base
#
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
