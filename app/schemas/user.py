from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    login_id: str | None = None
    password: str


class UserLogin(BaseModel):
    login_id: str | None = None
    username: str | None = None
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    number_of_posts: int = 0
