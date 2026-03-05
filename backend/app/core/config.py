import os
from pathlib import Path
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 1. Find the .env file reliably
# This assumes config.py is in backend/app/core/
# Adjust .parent calls to go up to your project root
# .parent.parent.parent go up 3 levels from 'core' -> 'app' -> 'backend' -> 'root'
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    # Load raw values
    DB_USER: str = os.getenv("user", "postgres")
    DB_PASSWORD: str = os.getenv("password", "")
    DB_HOST: str = os.getenv("host", "localhost")
    DB_PORT: str = os.getenv("port", "5432")
    DB_NAME: str = os.getenv("dbname", "postgres")
    SYSTEM_USER_ID: str = os.getenv("SYSTEM_USER_ID", "550e8400-e29b-41d4-a716-446655440000")

    # 2. Construct URL safely (handles special chars in password)
    @property
    def DATABASE_URL(self) -> str:
        # URL encode password to handle '@', ':', etc.
        encoded_pwd = quote_plus(self.DB_PASSWORD)
        return f"postgresql://{self.DB_USER}:{encoded_pwd}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        case_sensitive = False

settings = Settings()