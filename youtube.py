import re
import asyncio
from aiohttp import ClientSession
from pytube import YouTube
from fastapi import APIRouter

PATTERN = re.compile(r"watch\?v=(\S{11})")

YOUTUBE_URL = "https://www.youtube.com/watch?v="

SEARCH_URL = "https://www.youtube.com/results?search_query="

async def get_related_videos(url: str):
    """Get related videos from a YouTube video."""
    async with ClientSession() as session:
        async with session.get(url) as response:
           response = await response.text()
           _ = []
           for match in PATTERN.findall(response):
               _.append(match) if match not in _ else None
        return [f"{YOUTUBE_URL}{video_id}" for video_id in _]

async def get_video_info(url: str):
    """Get video info from a YouTube video."""
    yt = YouTube(url)
    return {
        "id": yt.video_id,
        "title": yt.title if yt.title else None,
        "author": yt.author if yt.author else None,
        "length": yt.length if yt.length else None,
        "views": yt.views if yt.views else None,
        "rating": yt.rating if yt.rating else None,
        "thumbnail": yt.thumbnail_url if yt.thumbnail_url else None,
        "embed_html": yt.embed_html if yt.embed_html else None,
        "caption": yt.captions.get_by_language_code("en") if yt.captions.get_by_language_code("en") else None,
    }
    
    
yt = APIRouter(prefix="/youtube", tags=["youtube"])

@yt.get("/related")    
async def related(url: str):
    """Get related videos from a YouTube video."""
    return await get_related_videos(url)

@yt.get("/info")
async def info(url: str):
    """Get video info from a YouTube video."""
    return await get_video_info(url)

@yt.get("/download")
async def download(id:str):
    """Download a YouTube video."""
    yt = YouTube(url=f"{YOUTUBE_URL}{id}")
    yt.streams.first().download(output_path="static/youtube")
    return {"url": f"/api/static/youtube/{yt.title}.mp4"}

@yt.get("/download/audio")
async def download_audio(url: str):
    """Download a YouTube video's audio."""
    yt = YouTube(url)
    yt.streams.filter(only_audio=True).first().download(output_path="static/youtube")
    return {"url": f"/api/static/youtube/{yt.title}.mp4"}

@yt.get("/download/playlist")
async def download_playlist(url: str):
    """Download a YouTube playlist."""
    yt = YouTube(url)
    yt.streams.first().download(output_path="static/youtube")
    return {"url": f"/api/static/youtube/{yt.title}.mp4"}

@yt.get("/download/playlist/audio")
async def download_playlist_audio(url: str):
    """Download a YouTube playlist's audio."""
    yt = YouTube(url)
    yt.streams.filter(only_audio=True).first().download(output_path="static/youtube")
    return {"url": f"/api/static/youtube/{yt.title}.mp4"}

@yt.get("/search")
async def search(query: str):
    """Search YouTube."""
    async with ClientSession() as session:
        async with session.get(f"{SEARCH_URL}{query}") as response:
            response = await response.text()
            _ = []
            for match in PATTERN.findall(response):
                _.append(match) if match not in _ else None
        urls = [f"{YOUTUBE_URL}{video_id}" for video_id in _]
        return await asyncio.gather(*[get_video_info(url) for url in urls])