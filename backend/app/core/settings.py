from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    # Database
    DATABASE_URL: str = 'postgresql+psycopg://user:password@localhost:5432/db'

    # App
    APP_URL: str = 'http://localhost:8000'
    INTERVAL_SYNC: int = 60  # Intervalo de execução dos jobs do scheduler
    DEBUG: bool = False

    # Telegram
    TELEGRAM_BOT_TOKEN: str = ''
    TELEGRAM_CHAT_ID: str = ''
    TELEGRAM_PYTHON_TOPIC_ID: str = ''
    TELEGRAM_JAVA_TOPIC_ID: str = ''
    TELEGRAM_GOLANG_TOPIC_ID: str = ''
    TELEGRAM_FRONTEND_TOPIC_ID: str = ''
    TELEGRAM_BACKEND_TOPIC_ID: str = ''
    TELEGRAM_MAX_MESSAGE_LENGTH: int = 4096

    # Discord
    DISCORD_BOT_ID: str = ''
    DISCORD_TOKEN: str = ''
    DISCORD_GUILD_ID: str = ''
    DISCORD_PYTHON_CHANNEL_ID: str = ''
    DISCORD_JAVA_CHANNEL_ID: str = ''
    DISCORD_GOLANG_CHANNEL_ID: str = ''
    DISCORD_FRONTEND_CHANNEL_ID: str = ''
    DISCORD_BACKEND_CHANNEL_ID: str = ''
    DISCORD_MAX_DESCRIPTION_LENGTH: int = 1024


@lru_cache
def get_settings():
    return Settings()
