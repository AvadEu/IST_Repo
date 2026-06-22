from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    discord_token: str = "dummy_token"
    discord_guild_id: str = "0"
    database_url: str = "sqlite+aiosqlite:////data/secretary.db"
    audio_dir: str = "/data/audio"
    web_host: str = "0.0.0.0"
    web_port: int = 80
    secret_key: str = "change_me"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
