from fastapi import APIRouter, HTTPException, Query, status, Depends
from app.schemas.bookmark import BookmarkCreate, BookmarkListResponse, BookmarkRead
from app.services.bookmark_service import BookmarkService
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(tags=["Bookmark"])

@router.get("", response_model=BookmarkListResponse)
async def list_bookmarks(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    return await BookmarkService.list(current_user.id, offset, limit)

@router.post("", response_model=BookmarkRead, status_code=status.HTTP_201_CREATED)
async def add_bookmark(payload: BookmarkCreate, current_user: User = Depends(get_current_user)):
    return await BookmarkService.add(current_user.id, payload.quote_id)

@router.delete("/{quote_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_bookmark(quote_id: int, current_user: User = Depends(get_current_user)):
    ok = await BookmarkService.remove(current_user.id, quote_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return await BookmarkService.remove(current_user.id, quote_id)
