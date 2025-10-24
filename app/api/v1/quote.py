
from fastapi import APIRouter

from app.models.quote import Quote

router = APIRouter(prefix="/quote", tags=["quote"])


@router.get("/random")
async def random_quote():
    q = await Quote.first()
    if not q:
        return {"id": 0, "content": "샘플 명언이 없습니다.", "author": None}
    return {"id": q.id, "content": q.content, "author": q.author}


@router.get("/")
async def list_quotes():
    qs = await Quote.all()
    return [{"id": q.id, "content": q.content, "author": q.author} for q in qs]
