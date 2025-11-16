# backend/app/core/config.py

import os
from typing import List

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Default to a mock key if not set, for local development without real API calls
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "mock-api-key-for-local-dev")
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
