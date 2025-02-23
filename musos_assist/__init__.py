from typing import Any
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from musos_assist.routers import singles_router

# from starlette.templating import _TemplateResponse

app = FastAPI(
    title="Music Single Release API",
    description="API for managing music single releases",
)


# Mount the static directory to serve static files
app.mount("/static", StaticFiles(directory="musos_assist/static"), name="static")


# Your API routes go here...
app.include_router(singles_router)


# If you need to serve the index.html at the root, you would generally
# do it by returning the file content.
@app.get("/", response_class=FileResponse)
async def read_simple_root() -> Any:
    return "musos_assist/static/index.html"
