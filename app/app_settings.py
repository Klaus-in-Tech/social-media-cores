from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):

    ORACLE_DB_USERNAME: str
    ORACLE_DB_PASSWORD: str
    ORACLE_DB_DSN: str

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()