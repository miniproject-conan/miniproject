from pydantic import BaseModel, ConfigDict, Field


class QuoteRead(BaseModel):
    id: int = Field(..., ge=1)
    author: str = Field(..., max_length=100)
    author_profile: str | None = Field(None, max_length=200)
    message: str = Field(..., min_length=1)

    model_config = ConfigDict(from_attributes=True)


class RandomQuoteResponse(BaseModel):
    data: QuoteRead

    model_config = ConfigDict(from_attributes=True)
