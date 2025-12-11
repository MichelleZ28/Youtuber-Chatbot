from typing import List, Dict, Optional, Any
import asyncio

class ChatService:
    def __init__(self, youtube_service, ai_service):
        self.youtube_service = youtube_service
        self.ai_service = ai_service
        self.channel_cache = {}
        self.conversations = {}
    
    async def process_message(
        self,
        youtube_url: str,
        user_message: str,
        chat_history: List[Dict[str, str]] = None
    ) -> Dict:
        """
        Process a user message and generate a response in the YouTuber's style
        
        Args:
            youtube_url: YouTube channel URL or ID
            user_message: The user's message
            chat_history: List of previous messages in the conversation
            
        Returns:
            Dictionary containing the response and conversation metadata
        """
        conversation_id = None
        try:
            # Extract channel ID from URL if needed
            channel_id = self._extract_channel_id(youtube_url)
            
            # Create a conversation ID based on the channel ID
            conversation_id = f"conv_{hash(channel_id) % 10000}"
            
            # Get or create conversation
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = {
                    'channel_id': channel_id,
                    'messages': [],
                    'context': {}
                }
            
            conversation = self.conversations[conversation_id]
            
            # Get channel info if not already in cache
            if channel_id not in self.channel_cache:
                channel_info = await self.youtube_service.get_channel_info(channel_id)
                self.channel_cache[channel_id] = channel_info
                
                # Add channel info to conversation context
                conversation['context'].update({
                    'channel_title': channel_info.get('title', ''),
                    'channel_description': channel_info.get('description', ''),
                    'videos': channel_info.get('videos', [])
                })
                
                # Get transcripts for some videos to understand the YouTuber's style
                video_samples = []
                for video in channel_info.get('videos', [])[:3]:  # Limit to first 3 videos
                    try:
                        transcript = await self.youtube_service.get_video_transcript(video['id'])
                        if transcript:
                            video_samples.append({
                                'title': video['title'],
                                'transcript': transcript[:2000]  # Limit transcript length
                            })
                    except Exception as e:
                        print(f"Error getting transcript for video {video['id']}: {str(e)}")
                
                # Add video samples to context
                conversation['context']['video_samples'] = video_samples
            
            # Add user message to conversation history
            conversation['messages'].append({
                'role': 'user',
                'content': user_message
            })
            
            # Generate AI response
            response = await self._generate_ai_response(conversation, chat_history or [])
            
            # Add AI response to conversation history
            conversation['messages'].append({
                'role': 'assistant',
                'content': response
            })
            
            return {
                'conversation_id': conversation_id,
                'response': response,
                'channel_info': self.channel_cache[channel_id]
            }
            
        except Exception as e:
            print(f"Error in chat service: {str(e)}")
            return {
                'conversation_id': conversation_id or 'error',
                'response': "I'm having trouble connecting to the YouTuber's content. Please try again later.",
                'channel_info': {},
                'error': str(e)
            }
    
    def _extract_channel_id(self, youtube_url: str) -> str:
        """Extract channel ID from YouTube URL"""
        # If it's already a channel ID (not a URL), return as is
        if not ('youtube.com' in youtube_url or 'youtu.be' in youtube_url):
            return youtube_url
            
        # Extract channel ID from URL
        # This is a simplified version - you might need to handle more URL formats
        if 'channel/' in youtube_url:
            return youtube_url.split('channel/')[-1].split('?')[0]
        elif 'youtube.com/c/' in youtube_url or 'youtube.com/user/' in youtube_url:
            return youtube_url.split('/')[-1].split('?')[0]
        else:
            # Default to using the URL as-is if we can't parse it
            return youtube_url
            
    async def _generate_ai_response(self, conversation: Dict, chat_history: List[Dict[str, str]]) -> str:
        """Generate AI response using the AI service"""
        # Build additional context string
        context_parts = []
        channel_title = conversation['context'].get('channel_title', '')
        channel_description = conversation['context'].get('channel_description', '')
        if channel_title:
            context_parts.append(f"Channel title: {channel_title}")
        if channel_description:
            context_parts.append(f"Channel description: {channel_description}")

        recent_videos = conversation['context'].get('videos', [])[:3]
        if recent_videos:
            recent_titles = ", ".join([video.get('title', '') for video in recent_videos if video.get('title')])
            if recent_titles:
                context_parts.append(f"Recent videos: {recent_titles}")

        additional_context = "\n".join(context_parts)

        # Combine provided chat history with stored conversation history (excluding latest user message)
        combined_history = (chat_history or []) + conversation['messages'][:-1]
        # Limit history to avoid excessive context
        combined_history = combined_history[-6:]

        # Generate style description
        youtuber_style = self._generate_youtuber_style(conversation['context'])

        prompt = conversation['messages'][-1]['content']

        response = await self.ai_service.generate_response(
            prompt=prompt,
            context=additional_context,
            conversation_history=combined_history,
            youtuber_style=youtuber_style
        )

        return response
    
    def _generate_conversation_id(self) -> str:
        """Generate a unique conversation ID"""
        import uuid
        return str(uuid.uuid4())
    
    def _generate_youtuber_style(self, context: Dict) -> str:
        """Generate a description of the YouTuber's style based on available context"""
        style_parts = []
        
        # Add channel description if available
        if context.get('channel_description'):
            style_parts.append(f"Channel description: {context['channel_description']}")
        
        # Add information from video transcripts
        if context.get('video_samples'):
            style_parts.append("The YouTuber's speaking style is characterized by:")
            
            # Analyze video titles for common topics
            topics = set()
            for video in context.get('videos', [])[:5]:
                title = video.get('title', '').lower()
                # Simple topic extraction (can be enhanced with NLP)
                if 'how to' in title:
                    topics.add("tutorial-style explanations")
                if 'review' in title:
                    topics.add("product reviews")
                if 'vs ' in title:
                    topics.add("comparisons")
                if '?' in title:
                    topics.add("question-and-answer format")
            
            if topics:
                style_parts.append(f"Common content types: {', '.join(topics)}.")
            
            # Add sample transcript excerpts
            style_parts.append("Sample of the YouTuber's speech patterns:")
            for i, video in enumerate(context.get('video_samples', [])[:2], 1):
                style_parts.append(f"From '{video['title']}': {video['transcript'][:300]}...")
        
        return "\n".join(style_parts)

