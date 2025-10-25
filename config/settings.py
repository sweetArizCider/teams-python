from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env', '.env.local')
    )

    mongodb_uri: str = Field(..., alias="MONGODB_URI")
    mongodb_database: str = Field(default="python-app", alias="MONGODB_DATABASE")
    mongodb_username: str = Field(..., alias="MONGODB_USERNAME")
    mongodb_password: str = Field(..., alias="MONGODB_PASSWORD")

_settings_instance = None

def get_settings() -> Settings:
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance

settings = get_settings()
