from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.quote import QuoteRead


class BookmarkCreate(BaseModel):
    quote_id: int = Field(...)


class BookmarkRead(BaseModel):
    id: int
    quote_id: int
    created_at: datetime
    quote: Optional[QuoteRead] = None

    model_config = ConfigDict(from_attributes=True)


class BookmarkListResponse(BaseModel):
    total: int = Field(...)
    items: List[BookmarkRead]

    model_config = ConfigDict(from_attributes=True)
