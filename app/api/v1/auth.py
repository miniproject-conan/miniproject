# app/api/v1/auth.py
# 회원가입 / 로그인 / 현재 사용자 조회

from fastapi import APIRouter, HTTPException, Depends, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
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

router = APIRouter(tags=["Auth"])
templates = Jinja2Templates(directory="app/templates")

# ------------------ 로그인 / 회원가입 화면 ------------------
@router.get("/login", response_class=HTMLResponse)
async def render_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/signin", response_class=HTMLResponse)
async def render_signin(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

# ------------------ 회원가입 / 로그인 / 토큰 ------------------
@router.post("/signup", response_model=UserResponse)
async def signup(user_data: UserCreate):
    if await User.filter(username=user_data.username).exists():
        raise HTTPException(status_code=400, detail="Username already taken")

    user = User(username=user_data.username, login_id=user_data.login_id)
    user.set_password(user_data.password)
    await user.save()
    return UserResponse(id=user.id, username=user.username, number_of_posts=user.number_of_posts)

@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, response: Response):
    try:
        # if user_data.login_id:
        #     user = await User.get(login_id=user_data.login_id)
        # elif user_data.username:
        #     user = await User.get(username=user_data.username)
        # else:
        #     raise DoesNotExist
        user = await User.get(login_id=user_data.login_id)
    except DoesNotExist:
        raise HTTPException(status_code=400, detail="Invalid username or login_id")

    if not user.verify_password(user_data.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    # ✅ 리다이렉트 대신 200 JSON + 쿠키 세팅
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=settings.JWT_ACCESS_MINUTES * 60,
        samesite="lax",
        path="/",
        # secure=True,  # HTTPS 배포 시 True로
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=settings.JWT_REFRESH_DAYS * 24 * 60 * 60,  # ✅ 일수 기준으로 수정
        samesite="lax",
        path="/",
        # secure=True,
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.JWT_ACCESS_MINUTES * 60,
        refresh_expires_in=settings.JWT_REFRESH_DAYS * 24 * 60 * 60,
    )

@router.post("/logout")
async def logout():
    response = RedirectResponse(url="/",status_code=302)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return response

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: TokenRefreshRequest, response: Response):
    user_id = decode_token(request.refresh_token, expected_type="refresh")
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)

    # ✅ 리프레시 시에도 쿠키 갱신
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=settings.JWT_ACCESS_MINUTES * 60,
        samesite="lax",
        path="/",
        # secure=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=settings.JWT_REFRESH_DAYS * 24 * 60 * 60,
        samesite="lax",
        path="/",
        # secure=True,
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.JWT_ACCESS_MINUTES * 60,
        refresh_expires_in=settings.JWT_REFRESH_DAYS * 24 * 60 * 60,
    )

@router.get("/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
    return current_user
