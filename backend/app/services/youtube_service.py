import os
from typing import Dict, List, Optional
import httpx
from youtubesearchpython import ChannelsSearch, Video
from youtube_transcript_api import YouTubeTranscriptApi
from ..config import settings

class YouTubeService:
    def __init__(self, api_key: str = None):
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.api_key = api_key or settings.YOUTUBE_API_KEY
        
    async def search_channel(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for YouTube channels by name or URL"""
        if not self.api_key:
            raise ValueError("YouTube API key is not configured")
            
        try:
            # First try to search using the query directly
            channels_search = ChannelsSearch(query, limit=max_results)
            results = channels_search.result()
            
            # Format the results
            channels = []
            for item in results.get('result', [])[:max_results]:
                channel = {
                    'id': item.get('id', ''),
                    'title': item.get('title', ''),
                    'description': item.get('description', ''),
                    'thumbnail': item.get('thumbnails', [{}])[0].get('url', '') if item.get('thumbnails') else '',
                    'subscriber_count': item.get('subscribers', ''),
                    'video_count': item.get('videos', 0)
                }
                channels.append(channel)
                
            return channels
            
        except Exception as e:
            raise Exception(f"Error searching for channels: {str(e)}")
    
    async def get_channel_info(self, channel_identifier: str) -> Dict:
        """Get detailed information about a YouTube channel.
        
        Args:
            channel_identifier: Can be a channel ID (starts with UC) or a handle (with or without @)
        """
        if not self.api_key:
            raise ValueError("YouTube API key is not configured")
            
        identifier = channel_identifier.strip()
        if identifier.startswith('@'):
            identifier = identifier[1:]
        if not identifier:
            raise ValueError("Channel identifier cannot be empty")

        try:
            async with httpx.AsyncClient() as client:
                if identifier.startswith('UC'):
                    channel_id = identifier
                else:
                    channel_id = await self._resolve_channel_id_from_handle(client, identifier)

                params = {
                    'part': 'snippet,statistics,contentDetails',
                    'id': channel_id,
                    'key': self.api_key
                }
                response = await client.get(
                    f"{self.base_url}/channels",
                    params=params
                )
                response.raise_for_status()
                data = response.json()

                if not data.get('items'):
                    raise ValueError("Channel not found")

                channel_data = data['items'][0]
                snippet = channel_data.get('snippet', {})
                stats = channel_data.get('statistics', {})

                uploads_playlist_id = channel_data.get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads')
                videos = []
                if uploads_playlist_id:
                    videos = await self.get_channel_videos(uploads_playlist_id, max_results=10)

                return {
                    'id': channel_data.get('id', ''),
                    'title': snippet.get('title', ''),
                    'description': snippet.get('description', ''),
                    'thumbnail': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                    'subscriber_count': stats.get('subscriberCount', '0'),
                    'video_count': stats.get('videoCount', '0'),
                    'view_count': stats.get('viewCount', '0'),
                    'videos': videos
                }

        except httpx.HTTPStatusError as e:
            error_msg = f"YouTube API error: {str(e)}"
            if e.response and e.response.status_code == 404:
                error_msg = f"Channel '{identifier}' not found"
            raise ValueError(error_msg)
        except ValueError:
            raise
        except Exception as e:
            raise Exception(f"Error getting channel info: {str(e)}")

    async def _resolve_channel_id_from_handle(self, client: httpx.AsyncClient, handle: str) -> str:
        """Resolve a YouTube channel ID using a handle or query."""
        search_params = {
            'part': 'snippet',
            'q': handle,
            'type': 'channel',
            'maxResults': 1,
            'key': self.api_key
        }
        search_url = f"{self.base_url}/search"
        search_response = await client.get(search_url, params=search_params)
        search_response.raise_for_status()
        search_data = search_response.json()

        items = search_data.get('items') or []
        if not items:
            raise ValueError(f"Channel '{handle}' not found")

        channel_id = items[0].get('id', {}).get('channelId')
        if not channel_id:
            raise ValueError(f"Channel '{handle}' not found")

        return channel_id
    
    async def get_channel_videos(self, playlist_id: str, max_results: int = 10) -> List[Dict]:
        """Get videos from a channel's uploads playlist"""
        if not self.api_key:
            raise ValueError("YouTube API key is not configured")
            
        try:
            async with httpx.AsyncClient() as client:
                # Get playlist items
                url = f"{self.base_url}/playlistItems"
                params = {
                    'part': 'snippet,contentDetails',
                    'playlistId': playlist_id,
                    'maxResults': max_results,
                    'key': self.api_key
                }
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                videos = []
                for item in data.get('items', []):
                    video_id = item.get('contentDetails', {}).get('videoId')
                    if not video_id:
                        continue
                        
                    snippet = item.get('snippet', {})
                    videos.append({
                        'id': video_id,
                        'title': snippet.get('title', ''),
                        'description': snippet.get('description', ''),
                        'published_at': snippet.get('publishedAt', ''),
                        'thumbnail': snippet.get('thumbnails', {}).get('high', {}).get('url', '')
                    })
                
                return videos
                
        except Exception as e:
            print(f"Error getting channel videos: {str(e)}")
            return []
    
    async def get_video_transcript(self, video_id: str) -> str:
        """Get transcript for a YouTube video."""
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            # Try to get the English transcript, fallback to the first available
            try:
                transcript = transcript_list.find_transcript(['en'])
            except:
                transcript = next(iter(transcript_list))
            transcript_text = " ".join([t['text'] for t in transcript.fetch()])
            return transcript_text
        except Exception as e:
            logger.error(f"Error getting transcript: {str(e)}")
            raise Exception("Could not get transcript for this video")

# Create a singleton instance
youtube_service = YouTubeService()
