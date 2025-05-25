"""Configuration settings for the FastAPI application."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "<<PROJECT_NAME>>"

    # Database Config
    database_url: str

    # Security
    secret_key: str = "NOT_SET"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    password_pepper: str = "NOT_SET"

    class Config:
        # Load environment variables from a .env file
        env_file = ".env"
        # Ignore extra environment variables not defined in Settings
        extra = "ignore"


settings = Settings()  # type: ignore[reportCallIssue]
