from typing import List
from musos_assist.domain.models import MusicSingleRelease


class MusicSingleReleaseRepository:
    def create_single(self, single: MusicSingleRelease) -> MusicSingleRelease:
        raise NotImplementedError

    def list_singles(self) -> List[MusicSingleRelease]:
        raise NotImplementedError

    def read_single(self, isrc: str) -> MusicSingleRelease:
        raise NotImplementedError

    def update_single(
        self, isrc: str, single_update: MusicSingleRelease
    ) -> MusicSingleRelease:
        raise NotImplementedError

    def delete_single(self, isrc: str) -> None:
        raise NotImplementedError
