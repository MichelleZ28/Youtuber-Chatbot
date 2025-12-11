import os
from typing import List, Dict, Optional
import openai
import tiktoken
from ..config import settings

class AIService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        self.temperature = settings.OPENAI_TEMPERATURE
        
        if not self.api_key:
            raise ValueError("OpenAI API key is not configured")
            
        openai.api_key = self.api_key
    
    async def generate_response(
        self,
        prompt: str,
        context: str = "",
        conversation_history: List[Dict] = None,
        youtuber_style: str = ""
    ) -> str:
        """
        Generate a response using OpenAI's API
        
        Args:
            prompt: The user's message
            context: Additional context about the YouTuber
            conversation_history: List of previous messages in the conversation
            youtuber_style: Description of the YouTuber's speaking style
            
        Returns:
            Generated response text
        """
        try:
            # Prepare messages with system and user context
            messages = []
            
            # Add system message with instructions
            system_message = (
                "You are an AI that mimics the style and personality of a specific YouTuber. "
                "Respond to the user's questions in a way that matches the YouTuber's tone, "
                "vocabulary, and speaking patterns. Be engaging and natural in your responses.\n\n"
            )
            
            if youtuber_style:
                system_message += f"YouTuber's style and background: {youtuber_style}\n\n"
                
            if context:
                system_message += f"Additional context about the YouTuber: {context}\n\n"
                
            system_message += (
                "Remember to keep your responses concise and in the first person perspective. "
                "If you don't know the answer to something, it's okay to say so in a way that "
                "matches the YouTuber's style."
            )
            
            messages.append({"role": "system", "content": system_message})
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history[-6:]:  # Limit history to last 6 messages
                    messages.append({"role": msg["role"], "content": msg["content"]})
            
            # Add the current user message
            messages.append({"role": "user", "content": prompt})
            
            # Call the OpenAI API
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            
            return response.choices[0].message['content'].strip()
            
        except Exception as e:
            print(f"Error generating AI response: {str(e)}")
            return "I'm having trouble generating a response right now. Please try again later."
    
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text string"""
        try:
            encoding = tiktoken.encoding_for_model(self.model)
            return len(encoding.encode(text))
        except:
            # Fallback for unknown models
            return len(text) // 4  # Rough estimate

# Create a singleton instance
ai_service = AIService()
