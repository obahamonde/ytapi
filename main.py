"""Main entrypoint for the application."""
from api.typedefs import (
    FastAPI,
    File,
    UploadFile,
    CORSMiddleware,
    JSONResponse,
    StaticFiles,
)

from fastapi.responses import (
    RedirectResponse,
    FileResponse,
    HTMLResponse,
)   

from api.youtube import yt

from api.video import vd


app = FastAPI(
    title="YouTube API",
    description="Author: @obahamonde [GitHub]",
    version="0.0.1",
    docs_url="/"
)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)
app.include_router(yt, prefix="/api")
app.include_router(vd, prefix="/api")
static = StaticFiles(directory="static", html=True)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)