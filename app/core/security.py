# app/core/security.py

from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import Depends, HTTPException, Request, Security, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.models.user import User

# ▶ 비밀번호 해시 (pbkdf2_sha256 사용 중)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# ▶ Swagger Authorize 버튼용 (헤더 Bearer 토큰을 붙여줌). auto_error=False로 두어도 됨.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

# ▶ 일반 요청의 Authorization: Bearer ... 헤더 파싱 (없어도 에러 안 나게)
http_bearer = HTTPBearer(auto_error=False)


def _salt_password(password: str) -> str:
    return f"{password}{settings.PASSWORD_SALT}"


def hash_password(password: str) -> str:
    return pwd_context.hash(_salt_password(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(_salt_password(plain_password), hashed_password)


def _create_token(
    subject: str,
    expires_delta: timedelta,
    token_type: str = "access",
    scopes: Optional[List[str]] = None,
) -> str:
    payload = {
        "sub": str(subject),
        "type": token_type,
        "scopes": scopes or [],
        "exp": datetime.utcnow() + expires_delta,
    }
    return jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


def create_access_token(user_id: int, scopes: Optional[List[str]] = None) -> str:
    return _create_token(
        str(user_id), timedelta(minutes=settings.JWT_ACCESS_MINUTES), "access", scopes
    )


def create_refresh_token(user_id: int, scopes: Optional[List[str]] = None) -> str:
    return _create_token(
        str(user_id), timedelta(days=settings.JWT_REFRESH_DAYS), "refresh", scopes
    )


def decode_jwt(token: str) -> dict:
    """JWT 디코딩 + 예외를 명확한 401로 변환."""
    try:
        return jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token expired"
        ) from e
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        ) from e


def decode_token(token: str, expected_type: str = "access") -> int:
    payload = decode_jwt(token)
    tok_type = payload.get("type", "access")
    if tok_type != expected_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
        )
    sub = payload.get("sub")
    try:
        return int(sub)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject"
        ) from e


def _extract_token(
    request: Request,
    bearer: Optional[HTTPAuthorizationCredentials],
    token_from_swagger: Optional[str],
) -> Optional[str]:
    """우선순위: 1) Authorization 헤더, 2) Swagger Authorize, 3) 쿠키(access_token/Authorization)."""
    # 1) 헤더: Authorization: Bearer <token>
    if bearer and bearer.credentials:
        return bearer.credentials

    # 2) Swagger Authorize 버튼으로 들어온 Bearer 토큰
    if token_from_swagger:
        # oauth2_scheme은 이미 'Bearer ' 제거된 순수 토큰을 줌
        return token_from_swagger

    # 3) 쿠키: access_token 또는 Authorization (혹시 Cookie에 'Bearer ...' 형태로 들어온 경우도 처리)
    cookie_token = request.cookies.get("access_token") or request.cookies.get(
        "Authorization"
    )
    if cookie_token:
        if isinstance(cookie_token, str) and cookie_token.startswith("Bearer "):
            return cookie_token.split(" ", 1)[1]
        return cookie_token

    return None


# ▶ 헤더/Swagger/쿠키 모두에서 토큰을 찾아 인증
async def get_current_user(
    request: Request,
    bearer: Optional[HTTPAuthorizationCredentials] = Security(http_bearer),
    token_from_swagger: Optional[str] = Depends(oauth2_scheme),
) -> User:
    token = _extract_token(request, bearer, token_from_swagger)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    user_id = decode_token(token, expected_type="access")
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user
