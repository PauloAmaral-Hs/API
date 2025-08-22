from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database - VPS PostgreSQL
    DATABASE_URL: str = "postgresql://postgres:1327a373e68cc300f1c5@easypanel.healthsafetytech.com:8000/ai_agents"
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    
    # App
    APP_NAME: str = "Movies API with AI"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
