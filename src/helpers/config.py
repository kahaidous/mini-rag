from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Mini RAG App"
    APP_VERSION: str = "0.1.0"
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    DB_NAME:str
    DB_CONNECTION:str

    class Config:
        env_file = ".env"

def get_settings() -> Settings:
    return Settings() 