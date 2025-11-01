# 환경 변수들을 pydantic BaseSettings로 관리하게 했습니다..
# .env 파일을 프로젝트 루트에 두면 자동으로 읽어오게 했습니다.
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):

    PROJECT_NAME: str = "Diary API"
    DATABASE_URL: str

    PASSWORD_SALT: str = ""
    JWT_SECRET_KEY: str = "your_jwt_secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_MINUTES: int = 60
    JWT_REFRESH_DAYS: int = 14

    DEBUG_MODE: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"), env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
