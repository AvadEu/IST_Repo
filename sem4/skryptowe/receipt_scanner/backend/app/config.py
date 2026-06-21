from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Konfiguracja aplikacji wczytywana ze zmiennych środowiskowych / .env."""

    db_url: str = "mysql+pymysql://receipts:receipts@mariadb:3306/receipts"
    upload_dir: str = "/uploads"
    secret_key: str = "change-me-in-production"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
