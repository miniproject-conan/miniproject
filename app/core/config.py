# 환경 변수들을 pydantic BaseSettings로 관리하게 했습니다..
# .env 파일을 프로젝트 루트에 두면 자동으로 읽어오게 했습니다.

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    PROJECT_NAME: str = "Diary API"

    # MySQL 연결 문자열
    # TORTOISE MYSQL 설치 후 사용 : pip install tortoise-orm[aiomysql]
    # TORTOISE postgreSQL 설치 후 사용 : pip install tortoise-orm[asyncpg]
    #
    DB_USER: str = "root"
    DB_PASSWORD: str = "1234"
    DB_HOST: str = "localhost"
    DB_PORT: str = "3306"
    DB_NAME: str = "diary_db"

    # postgre, mysql 모두 호환
    @property
    def database_url(self) -> str:
        if self.DB_TYPE == "mysql":
            return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        elif self.DB_TYPE == "postgresql":
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:
            raise ValueError("Unsupported DB_TYPE. Choose 'mysql' or 'postgresql'.")


    # SQLITE 연결
    # DATABASE_URL: str = "sqlite://db.sqlite3"
    PASSWORD_SALT: str = ""
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_MINUTES: int = 60
    JWT_REFRESH_DAYS: int = 14

    DEBUG_MODE: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
