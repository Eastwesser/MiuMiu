import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

dotenv_path = os.path.join(os.getcwd(), "venv", ".env")

load_dotenv(dotenv_path)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
    )

    bot_token: str
    admin_ids: frozenset[int] = frozenset({42, 5756911009})
    forecast_api: str = "YOUR_WEATHER_API_KEY_HERE"


settings = Settings()
