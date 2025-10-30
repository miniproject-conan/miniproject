from app.repositories.bookmark_repo import BookmarkRepository
from app.schemas.bookmark import BookmarkListResponse, BookmarkRead

class BookmarkService:
    @staticmethod
    async def add(user_id: int, quote_id: int) -> BookmarkRead:
        bm = await BookmarkRepository.add(user_id, quote_id)
        await bm.fetch_related("quote")
        return bm

    @staticmethod
    async def remove(user_id: int, quote_id: int) -> bool:
        deleted = await BookmarkRepository.remove(user_id, quote_id)
        return deleted > 0

    @staticmethod
    async def list(user_id: int, offset: int = 0, limit: int = 20) -> BookmarkListResponse:
        total, items = await BookmarkRepository.list_with_quotes(user_id, offset, limit)
        return BookmarkListResponse(
            total=total,
            items=[BookmarkRead.model_validate(i) for i in items],
        )
