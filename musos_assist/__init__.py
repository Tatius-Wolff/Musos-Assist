from typing import Any
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from musos_assist.routers import singles_router
import os

app = FastAPI(
    title="Music Single Release API",
    description="API for managing music single releases",
)

# Mount the static directory to serve static files
app.mount(
    "/static",
    StaticFiles(directory=(os.path.join(os.path.dirname(__file__), "static"))),
    name="static",
)

# Your API routes go here...
app.include_router(singles_router)


# Serve the index.html at the root
@app.get("/", response_class=FileResponse)
async def read_simple_root() -> Any:
    return FileResponse(
        path=os.path.join(os.path.dirname(__file__), "static", "index.html")
    )
