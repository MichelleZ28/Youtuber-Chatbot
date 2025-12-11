import os
from pathlib import Path
from pydantic import BaseSettings
from dotenv import load_dotenv

# Get the backend directory path
BACKEND_DIR = Path(__file__).parent.parent

# Load environment variables from .env file in the backend directory
load_dotenv(BACKEND_DIR / '.env')

class Settings(BaseSettings):
    # API Keys
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # App Settings
    APP_NAME: str = "YouTuber Chatbot"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]  # In production, replace with your frontend URL
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./youtuber_chatbot.db")
    
    # OpenAI Settings
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 1000
    
    class Config:
        case_sensitive = True

# Create settings instance
settings = Settings()
