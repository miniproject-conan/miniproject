from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.models.user import User
from app.models.quote import Quote

router = APIRouter(prefix="/bookmark", tags=["bookmark"])

@router.post("/{quote_id}")
async def add_bookmark(quote_id: int, user: User = Depends(get_current_user)):
    q = await Quote.filter(id=quote_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Quote not found")
    return {"message": "bookmarked", "quote_id": quote_id}

@router.delete("/{quote_id}")
async def remove_bookmark(quote_id: int, user: User = Depends(get_current_user)):
    q = await Quote.filter(id=quote_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Quote not found")
    return {"message": "unbookmarked", "quote_id": quote_id}

@router.get("/")
async def list_bookmarks(user: User = Depends(get_current_user)):
    return [{"quote_id": 1, "content": "삶은 뭘까"}]
