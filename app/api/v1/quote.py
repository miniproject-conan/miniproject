from fastapi import APIRouter, HTTPException

from app.schemas.quote import RandomQuoteResponse
from app.services.quote_service import QuoteService

router = APIRouter(prefix="/quote", tags=["Quote"])


@router.get("/", response_model=RandomQuoteResponse)
async def get_random_quote():
    try:
        return await QuoteService.get_random()
    except LookupError:
        raise HTTPException(status_code=404, detail="No quotes available")
