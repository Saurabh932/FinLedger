from functools import lru_cache # USed to cache the results of the functions
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "FinLedger"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding="utf-8",
        extra = "ignore",
    )

''' 
lru_cache is a decorator that caches the results of the function it decorates.
Which prevents us from repeatedly constructing the settings object.
'''
@lru_cache
def get_settings() -> Settings:
    return Settings()