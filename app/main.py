import uvicorn
from fastapi import FastAPI
from tortoise import Tortoise

from app.api.v1 import router as api_v1_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.on_event("startup")
async def init_orm() -> None:
    await Tortoise.init(db_url=settings.DATABASE_URL, modules={"models": ["app.models"]})
    await Tortoise.generate_schemas()


@app.on_event("shutdown")
async def close_orm() -> None:
    await Tortoise.close_connections()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG_MODE)
