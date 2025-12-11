from typing import Generator
from fastapi import Depends
from .services.youtube_service import YouTubeService
from .services.ai_service import AIService
from .services.chat_service import ChatService
from .config import settings

def get_youtube_service() -> YouTubeService:
    return YouTubeService(api_key=settings.YOUTUBE_API_KEY)

def get_ai_service() -> AIService:
    return AIService(api_key=settings.OPENAI_API_KEY)

def get_chat_service(
    youtube_service: YouTubeService = Depends(get_youtube_service),
    ai_service: AIService = Depends(get_ai_service)
) -> ChatService:
    return ChatService(youtube_service=youtube_service, ai_service=ai_service)
