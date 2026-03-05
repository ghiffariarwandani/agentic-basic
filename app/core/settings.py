import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "FastAPI Application"
    version: str = "1.0.0"
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")


settings = Settings()
