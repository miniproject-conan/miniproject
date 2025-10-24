from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.DATEBASE_URL, echo=True, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_= AsyncSession)

async def get_db():
    async with async_session() as session:
        yield session


async def init_db():
    from app.db.base import Base
    import app.models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)