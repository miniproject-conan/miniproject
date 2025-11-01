from app.repositories.quote_repo import QuoteRepository
from app.schemas.quote import QuoteRead, RandomQuoteResponse


class QuoteService:
    @staticmethod
    async def get_random() -> RandomQuoteResponse:
        q = await QuoteRepository.get_random()
        if not q:
            raise LookupError("No quotes available")
        return RandomQuoteResponse(data=QuoteRead.model_validate(q))
