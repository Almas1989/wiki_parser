from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str
    deepseek_api_key: str
    max_recursion_depth: int = 5

    class Config:
        env_file = ".env"
        extra = "ignore"  # ✅ разрешить лишние переменные


settings = Settings()