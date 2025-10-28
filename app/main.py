from fastapi import FastAPI
from app.core.config import settings
from app.db.session import init_db, close_db
from app.api.v1 import router as api_v1_router

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

@app.on_event("startup")
async def startup():
    await init_db(settings.DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await close_db()

app.include_router(api_v1_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
