from fastapi import APIRouter, Depends, HTTPException, status
from musos_assist.domain.models import MusicSingleRelease
from musos_assist.domain.ports import MusicSingleReleaseRepository
from musos_assist.adapters import (
    InMemoryMusicSingleReleaseRepository,
)

singles_router = APIRouter()
my_default_repository: MusicSingleReleaseRepository = (
    InMemoryMusicSingleReleaseRepository()
)


def get_repository() -> MusicSingleReleaseRepository:
    return my_default_repository


default_repository: MusicSingleReleaseRepository = Depends(get_repository)


@singles_router.post(
    "/singles/", response_model=MusicSingleRelease, status_code=status.HTTP_201_CREATED
)
async def create_single(
    single: MusicSingleRelease,
    repository: MusicSingleReleaseRepository = default_repository,
) -> MusicSingleRelease:
    try:
        return repository.create_single(single)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@singles_router.get("/singles/", response_model=list[MusicSingleRelease])
async def list_singles(
    repository: MusicSingleReleaseRepository = default_repository,
) -> list[MusicSingleRelease]:
    return repository.list_singles()


@singles_router.get("/singles/{isrc}", response_model=MusicSingleRelease)
async def read_single(
    isrc: str, repository: MusicSingleReleaseRepository = default_repository
) -> MusicSingleRelease:
    try:
        return repository.read_single(isrc)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@singles_router.put("/singles/{isrc}", response_model=MusicSingleRelease)
async def update_single(
    isrc: str,
    single_update: MusicSingleRelease,
    repository: MusicSingleReleaseRepository = default_repository,
) -> MusicSingleRelease:
    try:
        return repository.update_single(isrc, single_update)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@singles_router.delete("/singles/{isrc}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_single(
    isrc: str, repository: MusicSingleReleaseRepository = default_repository
) -> None:
    try:
        repository.delete_single(isrc)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
