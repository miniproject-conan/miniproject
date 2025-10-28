# TortoiseORM User 모델 비밀번호는 hashed_password에 저장하게했습니다.

from tortoise import fields
from tortoise.models import Model
from passlib.context import CryptContext
from hashlib import sha256
from app.core.config import settings

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    login_id = fields.CharField(max_length=50, unique=True, null=True)
    hashed_password = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    number_of_posts = fields.IntField(default=0)
    posts = fields.ReverseRelation["Post"]

    def __str__(self) -> str:
        return self.username

    def _salt_password(self, password: str) -> str:
        
        salted = f"{password}{settings.PASSWORD_SALT}".encode("utf-8")
        return sha256(salted).hexdigest()

    def set_password(self, password: str) -> None:
        
        self.hashed_password = pwd_context.hash(self._salt_password(password))

    def verify_password(self, password: str) -> bool:
        
        return pwd_context.verify(self._salt_password(password), self.hashed_password)
