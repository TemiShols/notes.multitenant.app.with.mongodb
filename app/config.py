# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    MONGODB_URI: str = Field(default="mongodb://localhost:27017")
    DB_NAME: str = Field(default="notes_multi_tenant")
    HEADER_ORG: str = Field(default="X-Org-ID")
    HEADER_USER: str = Field(default="X-User-ID")

    # Pydantic v2 config
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
