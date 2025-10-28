from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

class AuthService:
    async def register(self, email: str, password: str):
        hashed = hash_password(password)
        return await User.create(email=email, password=hashed)

    async def authenticate(self, email: str, password: str):
        user = await User.get_or_none(email=email)
        if not user or not verify_password(password, user.password):
            return None
        token = create_access_token({"sub": str(user.id)})
        return token
