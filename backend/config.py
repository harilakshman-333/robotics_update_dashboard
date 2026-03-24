from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    XAI_API_KEY: str
    GEMINI_API_KEY: str
    GMAIL_USER: str
    GMAIL_APP_PASSWORD: str
    DATABASE_URL: str
    REDIS_URL: str
    CELERY_BROKER_URL: str = ""
    APIFY_API_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache
def get_settings() -> Settings:
    return Settings()
