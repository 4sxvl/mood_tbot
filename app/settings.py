from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    bot_token: str = ""
    bot_proxy: str = ""
    g_creds_path: Path = Path(".secrets/g_creds.json")
    g_spread_key: str = ""
    admin_tg_ids: list[int] = []


settings = Settings()
