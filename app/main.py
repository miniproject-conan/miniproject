from fastapi import FastAPI
from app.core.config import settings
from app.db.session import init_db, close_db

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

@app.on_event("startup")
async def startup():
    await init_db(settings.DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await close_db()

@app.get("/health")
async def health_check():
    return {"status": "ok"}
