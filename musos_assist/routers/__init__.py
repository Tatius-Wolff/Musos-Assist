from typing import List, Union, Any
import logging
import os
from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError
from musos_assist.models.pydantic import MusicSingleRelease
from musos_assist.constants import SINGLE_NOT_FOUND, EXAMPLE_SINGLE_DATA


# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.WARNING),
    format="%(asctime)s - %(levelname)s - %(message)s",
)


singles_router = APIRouter()

# Example Usage Data (for testing via API client like curl or Postman)
example_single = MusicSingleRelease(**EXAMPLE_SINGLE_DATA)

# In-memory database (replace with a real database in production)
singles_db: dict[str, MusicSingleRelease] = {}  # example_single.isrc: example_single}


@singles_router.post(
    "/singles/", response_model=MusicSingleRelease, status_code=status.HTTP_201_CREATED
)
async def create_single(
    single: Union[MusicSingleRelease, dict[str, Any]],
) -> MusicSingleRelease:
    """
    Create a new music single release.
    """
    if isinstance(single, dict):
        try:
            single = MusicSingleRelease(**single)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors()
            )
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
            status_code=status.HTTP_404_NOT_FOUND, detail=SINGLE_NOT_FOUND
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
            status_code=status.HTTP_404_NOT_FOUND, detail=SINGLE_NOT_FOUND
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
            status_code=status.HTTP_404_NOT_FOUND, detail=SINGLE_NOT_FOUND
        )
    del singles_db[isrc]
    return None  # 204 No Content - no response body
