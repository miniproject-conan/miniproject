from tortoise.exceptions import IntegrityError, DoesNotExist
from app.models.bookmark import Bookmark
from app.models.quote import Quote

class BookmarkRepository:
    @staticmethod
    async def add(user_id: int, quote_id: int) -> Bookmark:
        await Quote.get(id=quote_id)
        try:
            bm = await Bookmark.create(user_id=user_id, quote_id=quote_id)
        except IntegrityError:
            bm = await Bookmark.get(user_id=user_id, quote_id=quote_id)
        return bm

    @staticmethod
    async def remove(user_id: int, quote_id: int) -> int:
        deleted = await Bookmark.filter(user_id=user_id, quote_id=quote_id).delete()
        return deleted

    @staticmethod
    async def list_with_quotes(user_id: int, offset=0, limit=20):
        qs = Bookmark.filter(user_id=user_id).select_related("quote").order_by("-created_at")
        total = await qs.count()
        items = await qs.offset(offset).limit(limit)
        return total, list(items)
