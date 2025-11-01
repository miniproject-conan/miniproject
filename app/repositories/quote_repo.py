import random

from app.models.quote import Quote


class QuoteRepository:
    @staticmethod
    async def get_random() -> Quote | None:
        total = await Quote.all().count()
        if total == 0:
            return None
        offset = random.randint(0, total - 1)
        return await Quote.all().offset(offset).limit(1).first()
