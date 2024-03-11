from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
    )

    bot_token: str
    admin_ids: frozenset[int] = frozenset({42, 5756911009})
    forecast_api: str = "YOUR_WEATHER_API_KEY_HERE"


settings = Settings()
