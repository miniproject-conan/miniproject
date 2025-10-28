from app.repositories.bookmark_repo import BookmarkRepository
from app.schemas.bookmark import BookmarkListResponse, BookmarkRead

class BookmarkService:
    @staticmethod
    async def add(quote_id: int) -> BookmarkRead:
        bm = await BookmarkRepository.add(quote_id)
        bm = await bm.fetch_related("quote")
        return BookmarkRead.model_validate(bm)

    @staticmethod
    async def remove(quote_id: int) -> bool:
        deleted = await BookmarkRepository.remove_by_quote_id(quote_id)
        return deleted > 0

    @staticmethod
    async def list(offset: int = 0, limit: int = 20) -> BookmarkListResponse:
        total, items = await BookmarkRepository.list_with_quotes(offset, limit)
        return BookmarkListResponse(
            total=total,
            items=[BookmarkRead.model_validate(i) for i in items],
        )
