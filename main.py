"""Main entrypoint for the application."""
from imports.dev import (
    FastAPI,
    File,
    UploadFile,
    CORSMiddleware,
    JSONResponse,
    StaticFiles,
)

from youtube import yt

from video import vd

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)
app.include_router(yt, prefix="/api")
app.include_router(vd, prefix="/api")
static = StaticFiles(directory="static", html=True)


@app.get("/api")
async def root():
    """Root endpoint."""
    return {"message": "PyOBS"}


@app.post("/api/upload")
async def upload(key: str, file: UploadFile = File(...)):
    """Upload endpoint."""
    _ = await file.read()
    with open(f"static/{key}/{file.filename}", "wb") as f:
        f.write(_)
    url = f"/api/static/{key}/{file.filename}"
    print(url)
    return JSONResponse({"url": url})


app.mount("/api/static", static, name="static")
