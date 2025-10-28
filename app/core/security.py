# Swagger의 "Authorize" 버튼을 위해 tokenUrl은 실제 로그인 엔드포인트로 맞춰둠.

from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext

from app.core.config import settings
from app.models.user import User


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
http_bearer = HTTPBearer(auto_error=True)

def _salt_password(password: str) -> str:
    return f"{password}{settings.PASSWORD_SALT}"

def hash_password(password: str) -> str:
    return pwd_context.hash(_salt_password(password))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(_salt_password(plain_password), hashed_password)

def _create_token(subject: str, expires_delta: timedelta, token_type: str = "access", scopes: Optional[List[str]] = None) -> str:
    payload = {
        "sub": str(subject),
        "type": token_type,
        "scopes": scopes or [],
        "exp": datetime.utcnow() + expires_delta,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def create_access_token(user_id: int, scopes: Optional[List[str]] = None) -> str:
    return _create_token(str(user_id), timedelta(minutes=settings.JWT_ACCESS_MINUTES), token_type="access", scopes=scopes)

def create_refresh_token(user_id: int, scopes: Optional[List[str]] = None) -> str:
    return _create_token(str(user_id), timedelta(days=settings.JWT_REFRESH_DAYS), token_type="refresh", scopes=scopes)

def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

def decode_token(token: str, expected_type: str = "access") -> int:
    payload = decode_jwt(token)
    tok_type = payload.get("type", "access")
    if tok_type != expected_type:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
    sub = payload.get("sub")
    try:
        return int(sub)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")
#
# async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
#     user_id = decode_token(token, expected_type="access")
#     user = await User.filter(id=int(user_id)).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
#     return user


async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(http_bearer)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        token_type = payload.get("type")
        # scopes = payload.get("scopes",[])
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token")
        if token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Wrong token type")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials")

    try:
        user_id = int(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    user = await User.get_or_none(id=int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found")
    return user