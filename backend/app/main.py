import os
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any
import logging
import time

from app.services.youtube_service import YouTubeService
from app.services.ai_service import AIService
from app.services.chat_service import ChatService
from app.config import settings
from app.api.endpoints import router as api_router

# Create FastAPI app with OpenAPI configuration
app = FastAPI(
    title="YouTuber Chatbot API",
    description="API for chatting with AI that mimics YouTubers",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
youtube_service = YouTubeService(api_key=settings.YOUTUBE_API_KEY)
ai_service = AIService(api_key=settings.OPENAI_API_KEY)
chat_service = ChatService(youtube_service, ai_service)

# Include API router
app.include_router(api_router, prefix="/api")

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    
    # Log response
    logger.info(f"Response: {response.status_code} in {process_time:.2f}ms")
    
    return response

# Pydantic models
class ChatMessage(BaseModel):
    content: str
    role: str = "user"

class ChatRequest(BaseModel):
    youtube_url: str
    message: str
    chat_history: List[Dict[str, str]] = []

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to YouTuber Chatbot API",
        "docs": "/api/docs",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "version": "1.0.0",
        "environment": "development" if settings.DEBUG else "production"
    }


@app.get("/api/youtube/channel")
async def get_channel_info(url: str):
    """Get information about a YouTube channel"""
    try:
        channel_info = await youtube_service.get_channel_info(url)
        return channel_info
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

@app.get("/api/test-ai")
async def test_ai(message: str = "Hello, how are you?"):
    try:
        response = await ai_service.generate_response(message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )
