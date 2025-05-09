import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    DB_NAME: str
    HOST: str
    PORT: int
    DEBUG: bool

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )

def get_db_url() -> str:
    return f"sqlite+aiosqlite:///{(BASE_DIR / settings.DB_NAME).as_posix()}"

settings = Settings()
