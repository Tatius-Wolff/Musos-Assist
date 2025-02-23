from typing import List, Any
import logging
import os
from fastapi import FastAPI, HTTPException, status
from musos_assist.musicsinglerelease import MusicSingleRelease


# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.WARNING),
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# FIXME: pydantic_core._pydantic_core.ValidationError: 1 validation error for Crew Value error, Please provide an
# OpenAI API key.
# Need to set false OPENAI_API_KEY to a non-empty string to avoid this error using memory=True on your Crew()
# if not os.environ.get("OPENAI_API_KEY"):
#     os.environ["OPENAI_API_KEY"] = "N/A"


app = FastAPI(
    title="Music Single Release API",
    description="API for managing music single releases",
)

# In-memory database (replace with a real database in production)
singles_db = {}


@app.post(
    "/singles/", response_model=MusicSingleRelease, status_code=status.HTTP_201_CREATED
)
async def create_single(single: MusicSingleRelease) -> MusicSingleRelease:
    """
    Create a new music single release.
    """
    if single.isrc in singles_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ISRC already exists"
        )
    singles_db[single.isrc] = single
    return single


@app.get("/singles/", response_model=List[MusicSingleRelease])
async def list_singles() -> list[Any]:
    """
    List all music single releases.
    """
    return list(singles_db.values())


@app.get("/singles/{isrc}", response_model=MusicSingleRelease)
async def read_single(isrc: str) -> Any:
    """
    Get a music single release by its ISRC.
    """
    if isrc not in singles_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Single not found"
        )
    return singles_db[isrc]


@app.put("/singles/{isrc}", response_model=MusicSingleRelease)
async def update_single(
    isrc: str, single_update: MusicSingleRelease
) -> MusicSingleRelease:
    """
    Update an existing music single release.
    """
    print("***", isrc, "***")
    if isrc != single_update.isrc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ISRC in path and request body do not match",
        )
    if isrc not in singles_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Single not found"
        )
    singles_db[isrc] = single_update  # Replace the existing single with the updated one
    return single_update


@app.delete("/singles/{isrc}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_single(isrc: str) -> None:
    """
    Delete a music single release by its ISRC.
    """
    if isrc not in singles_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Single not found"
        )
    del singles_db[isrc]
    return None  # 204 No Content - no response body
