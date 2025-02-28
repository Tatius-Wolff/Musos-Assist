from typing import List
from musos_assist.domain.models import MusicSingleRelease
from musos_assist.domain.ports import MusicSingleReleaseRepository
from musos_assist.constants import SINGLE_NOT_FOUND


class InMemoryMusicSingleReleaseRepository(MusicSingleReleaseRepository):
    def __init__(self) -> None:
        self.singles_db: dict[str, MusicSingleRelease] = {}

    def create_single(self, single: MusicSingleRelease) -> MusicSingleRelease:
        if single.isrc in self.singles_db:
            raise ValueError("ISRC already exists")
        self.singles_db[single.isrc] = single
        return self.singles_db[single.isrc]

    def list_singles(self) -> List[MusicSingleRelease]:
        return list(self.singles_db.values())

    def read_single(self, isrc: str) -> MusicSingleRelease:
        if isrc not in self.singles_db:
            raise ValueError(SINGLE_NOT_FOUND)
        return self.singles_db[isrc]

    def update_single(
        self, isrc: str, single_update: MusicSingleRelease
    ) -> MusicSingleRelease:
        # if isrc != single_update.isrc:
        #     raise ValueError("ISRC in path and request body do not match")
        if isrc not in self.singles_db:
            raise ValueError(SINGLE_NOT_FOUND)
        # AI! remove item from dict and re-add it to update the value and new isrc
        del self.singles_db[isrc]
        self.singles_db[single_update.isrc] = single_update
        return self.singles_db[single_update.isrc]

    def delete_single(self, isrc: str) -> None:
        if isrc not in self.singles_db:
            raise ValueError(SINGLE_NOT_FOUND)
        del self.singles_db[isrc]
