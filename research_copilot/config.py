from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    index_path: Path = Path("data/index/index.json")
    generator_provider: str = "extractive"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    min_confidence: float = 0.12

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
