from typing import List, Any
import logging
import os
from fastapi import APIRouter, HTTPException, status
from musos_assist.musicsinglerelease import MusicSingleRelease


# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.WARNING),
    format="%(asctime)s - %(levelname)s - %(message)s",
)


singles_router = APIRouter()

# Example Usage Data (for testing via API client like curl or Postman)
EXAMPLE_SINGLE_DATA: dict[str, Any] = {
    "title": "My Awesome Song",
    "isrc": "USX9P2400001",
    "artist_names": ["My Band"],
    "release_date": "2024-01-15",
    "genres": ["Rock", "Indie"],
    "label": "Independent Label",
    "version": "Original",
    "formats": ["Digital", "Vinyl"],
    "duration": "00:03:45",  # ISO 8601 duration format might be better in real-world, or seconds/minutes
    "artwork_url": "https://example.com/artwork.jpg",
    "audio_preview_url": "https://example.com/preview.mp3",
    "catalog_number": "MBR001",
    "subgenres": ["Alternative Rock"],
    "composers": ["John Doe", "Jane Smith"],
    "producers": ["Producer Y"],
    "language": "English",
    "lyrics": "Lyrics go here,\nThis is my song,\nThis is a cool song.",
    "notes": "Debut single.",
}

# In-memory database (replace with a real database in production)
singles_db = {}  # EXAMPLE_SINGLE_DATA["isrc"]: EXAMPLE_SINGLE_DATA}


@singles_router.post(
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


@singles_router.get("/singles/", response_model=List[MusicSingleRelease])
async def list_singles() -> list[Any]:
    """
    List all music single releases.
    """
    return list(singles_db.values())


@singles_router.get("/singles/{isrc}", response_model=MusicSingleRelease)
async def read_single(isrc: str) -> Any:
    """
    Get a music single release by its ISRC.
    """
    if isrc not in singles_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Single not found"
        )
    return singles_db[isrc]


@singles_router.put("/singles/{isrc}", response_model=MusicSingleRelease)
async def update_single(
    isrc: str, single_update: MusicSingleRelease
) -> MusicSingleRelease:
    """
    Update an existing music single release.
    """
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


@singles_router.delete("/singles/{isrc}", status_code=status.HTTP_204_NO_CONTENT)
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
