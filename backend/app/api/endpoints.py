from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Dict, Optional
from pydantic import BaseModel
from app.dependencies import get_chat_service, get_youtube_service
from app.services.chat_service import ChatService
from app.services.youtube_service import YouTubeService

router = APIRouter()

# Request/Response Models
class Message(BaseModel):
    content: str
    role: str  # 'user' or 'assistant'

class ChatRequest(BaseModel):
    youtube_url: str
    message: str
    chat_history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    channel_info: Dict

class SearchRequest(BaseModel):
    query: str
    max_results: int = 5

class ChannelInfo(BaseModel):
    id: str
    title: str
    description: str
    thumbnail: str
    subscriber_count: str
    video_count: str

# Endpoints
@router.post("/search", response_model=List[ChannelInfo])
async def search_channels(
    request: SearchRequest,
    youtube_service: YouTubeService = Depends(get_youtube_service)
):
    """
    Search for YouTube channels by name or URL
    """
    try:
        results = youtube_service.search_channels(request.query, request.max_results)
        return [ChannelInfo(**channel) for channel in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/channels/{channel_identifier}", response_model=ChannelInfo)
async def get_channel(
    channel_identifier: str,
    youtube_service: YouTubeService = Depends(get_youtube_service)
):
    """
    Get detailed information about a YouTube channel.
    Can use channel ID (UC...) or handle (with or without @)
    """
    try:
        channel_info = await youtube_service.get_channel_info(channel_identifier)
        if not channel_info:
            raise HTTPException(status_code=404, detail="Channel not found")
        return ChannelInfo(**channel_info)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat", response_model=ChatResponse)
async def chat_with_youtuber(
    chat_request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Chat with an AI that mimics a YouTuber's style
    """
    try:
        response = await chat_service.process_message(
            youtube_url=chat_request.youtube_url,
            user_message=chat_request.message,
            chat_history=chat_request.chat_history
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Get conversation history by ID
    """
    if conversation_id in chat_service.conversations:
        return {
            'conversation_id': conversation_id,
            'messages': chat_service.conversations[conversation_id]['messages']
        }
    raise HTTPException(status_code=404, detail="Conversation not found")