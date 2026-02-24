from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    # Database
    DATABASE_URL: str = 'postgresql+psycopg://user:password@localhost:5432/db'

    # App
    INTERVAL_SYNC: int = 60  # intervalo em minutos para busca de novas vagas


@lru_cache
def get_settings():
    return Settings()
