import os
from pathlib import Path
from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve project root once at module import time. Keep it outside the
# Settings class so Pydantic doesn't treat it as an un-annotated model field.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    # Application Settings (all from .env)
    PROJECT_NAME: str
    APP_ENV: str
    APP_HOST: str
    APP_PORT: int
    STAGE_PATH: str

    # Database Settings (all from .env)
    DB_URL: AnyUrl

    # Database Connection Pool Settings (all from .env)
    DB_POOL_SIZE: int
    DB_MAX_OVERFLOW: int
    DB_POOL_TIMEOUT: int
    DB_POOL_RECYCLE: int

    # Security Settings (all from .env)
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Logging Settings (from .env)
    LOG_LVL: str

    # Email Settings (Gmail SMTP)
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str
    SMTP_FROM_NAME: str

    # Email Settings (SendGrid)
    SENDGRID_API_KEY: str
    SENDGRID_FROM_EMAIL: str
    SENDGRID_FROM_NAME: str

    # OTP Settings
    OTP_EXPIRE_MINUTES: int
    OTP_LENGTH: int
       
    # pydantic v2 style configuration
    # Use the module-level PROJECT_ROOT so Pydantic doesn't treat this as
    # a model field (avoids non-annotated attribute errors).
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra='ignore'
    )



settings = Settings()
