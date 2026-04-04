import os
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DB_USER: str = os.getenv("user", "postgres")
    DB_PASSWORD: str = os.getenv("password", "")
    DB_HOST: str = os.getenv("host", "localhost")
    DB_PORT: str = os.getenv("port", "5432")
    DB_NAME: str = os.getenv("dbname", "postgres")
    SYSTEM_USER_ID: str = os.getenv("SYSTEM_USER_ID", "550e8400-e29b-41d4-a716-446655440000")

    @property
    def DATABASE_URL(self) -> str:
        encoded_pwd = quote_plus(self.DB_PASSWORD)
        return f"postgresql://{self.DB_USER}:{encoded_pwd}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        case_sensitive = False


settings = Settings()
