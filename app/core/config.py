from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):

    PROJECT_NAME: str
    DATABASE_URL: str

    PASSWORD_SALT: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_MINUTES: int = 60
    JWT_REFRESH_DAYS: int = 14

    DEBUG_MODE: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )



settings = Settings()