from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    # Database
    DATABASE_URL: str = 'postgresql+psycopg://user:password@localhost:5432/db'

    # App
    INTERVAL_SYNC: int = 30  # Intervalo de execução dos jobs do scheduler

    # Telegram
    TELEGRAM_BOT_TOKEN: str = ''
    TELEGRAM_CHAT_ID: str = ''
    TELEGRAM_PYTHON_TOPIC_ID: str = '3'
    TELEGRAM_JAVA_TOPIC_ID: str = '5'
    TELEGRAM_GOLANG_TOPIC_ID: str = '6'
    TELEGRAM_FRONTEND_TOPIC_ID: str = '8'
    TELEGRAM_BACKEND_TOPIC_ID: str = '7'


@lru_cache
def get_settings():
    return Settings()
