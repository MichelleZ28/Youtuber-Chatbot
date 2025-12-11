"""
API endpoints for the YouTuber Chatbot application.

This module contains all the API routes and request/response models.
"""

from fastapi import APIRouter

# Create main API router
router = APIRouter()

# Import all endpoint modules here to register their routes
from . import endpoints  # noqa: F401

# Include all endpoints in the router
router.include_router(endpoints.router, tags=["youtuber-chatbot"])

__all__ = ["router"]
