from typing import List
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip
from moviepy.video.fx import all as vfx
from moviepy.audio.fx import all as afx
from moviepy.video.tools.subtitles import SubtitlesClip
from fastapi import APIRouter

vd = APIRouter(prefix="/video", tags=["video"])

@vd.get("/crop")
async def crop(url: str, name: str, start: int, end: int):
    """Crop a video."""
    clip = VideoFileClip(url)
    clip = clip.subclip(start, end)
    clip.write_videofile(f"static/video/{name}.mp4")
    return {"url": f"/api/static/video/{name}.mp4"}