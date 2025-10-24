# 회원가입 / 로그인 / 현재 사용자 조회 

from fastapi import APIRouter, HTTPException, Depends
from tortoise.exceptions import DoesNotExist

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.token import TokenResponse, TokenRefreshRequest
from app.core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token,
    decode_token, get_current_user
)
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserResponse)
async def signup(user_data: UserCreate):
    if await User.filter(username=user_data.username).exists():
        raise HTTPException(status_code=400, detail="Username already taken")

    user = User(username=user_data.username, login_id=user_data.login_id)
    user.set_password(user_data.password)
    await user.save()
    return UserResponse(id=user.id, username=user.username, number_of_posts=user.number_of_posts)

@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin):
    try:
        if user_data.login_id:
            user = await User.get(login_id=user_data.login_id)
        elif user_data.username:
            user = await User.get(username=user_data.username)
        else:
            raise DoesNotExist
    except DoesNotExist:
        raise HTTPException(status_code=400, detail="Invalid username or login_id")

    if not user.verify_password(user_data.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.JWT_ACCESS_MINUTES * 60,
        refresh_expires_in=settings.JWT_REFRESH_DAYS * 24 * 60 * 60
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: TokenRefreshRequest):
    user_id = decode_token(request.refresh_token, expected_type="refresh")
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.JWT_ACCESS_MINUTES * 60,
        refresh_expires_in=settings.JWT_REFRESH_DAYS * 24 * 60 * 60
    )

@router.get("/me", response_model=UserResponse)
async def get_me(user = Depends(get_current_user)):
    return UserResponse(id=user.id, username=user.username, number_of_posts=user.number_of_posts)
