from fastapi import APIRouter

vd = APIRouter(prefix="/video", tags=["video"])

@vd.get("/crop")
async def crop(url: str, name: str, start: int, end: int):
    """Crop a video."""
    return {
        "error": "Not implemented yet."
    }