# 환경 변수들을 pydantic BaseSettings로 관리하게 했습니다..
# .env 파일을 프로젝트 루트에 두면 자동으로 읽어오게 했습니다.
# JWT, DB, 서버 환경을 한곳에서 관리

import os
from pydantic_setting import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):

    # 기본 설정
    PROJECT_NAME: str = "Diary API"
    DEBUG_MODE: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # 데이터베이스 설정
    DATABASE_URL: str = Field(default="sqlite://db.sqlite3", env="DATABASE_URL")

    # 보안 및 암호화 관련 설정
    PASSWORD_SALT: str = Field(default="some-random-string", env="PASSWORD_SALT")
    JWT_SECRET_KEY: str = Field(default="your-secret-key", env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"

    # 토큰 만료 설정
    JWT_ACCESS_MINUTES: int = Field(default=60, env="JWT_ACCESS_MINUTES")
    JWT_REFRESH_DAYS: int = Field(default=14, env="JWT_REFRESH_DAYS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

# 세팅 인스턴스 설정 (다른 모듈에서 import)
settings = Settings()
