import pytest
from musos_assist.domain.ports import MusicSingleReleaseRepository
from musos_assist.domain.models import MusicSingleRelease
from musos_assist.adapters import InMemoryMusicSingleReleaseRepository
from musos_assist.constants import EXAMPLE_SINGLE_DATA, SINGLE_NOT_FOUND


def test_list_singles_empty() -> None:
    repository: MusicSingleReleaseRepository = InMemoryMusicSingleReleaseRepository()
    assert isinstance(repository, MusicSingleReleaseRepository)
    assert repository.list_singles() == []


def test_create_single() -> None:
    repository: MusicSingleReleaseRepository = InMemoryMusicSingleReleaseRepository()
    single = MusicSingleRelease(**EXAMPLE_SINGLE_DATA.copy())
    created_single = repository.create_single(single)
    assert created_single == single


def test_create_single_duplicate_isrc() -> None:
    repository: MusicSingleReleaseRepository = InMemoryMusicSingleReleaseRepository()
    single1 = MusicSingleRelease(**EXAMPLE_SINGLE_DATA.copy())
    single1.isrc = "US1234567890"
    repository.create_single(single1)
    single2 = MusicSingleRelease(**EXAMPLE_SINGLE_DATA.copy())
    single2.isrc = "US1234567890"  # Duplicate ISRC
    with pytest.raises(ValueError, match="ISRC already exists"):
        repository.create_single(single2)


def test_list_singles() -> None:
    repository: MusicSingleReleaseRepository = InMemoryMusicSingleReleaseRepository()
    single1 = MusicSingleRelease(**EXAMPLE_SINGLE_DATA.copy())
    single1.isrc = "US1234567890"
    single1.title = "Test Single 1"
    single2 = MusicSingleRelease(**EXAMPLE_SINGLE_DATA.copy())
    single2.isrc = "US0987654321"
    single2.title = "Test Single 2"
    repository.create_single(single1)
    repository.create_single(single2)
    assert repository.list_singles() == [single1, single2]


def test_read_single() -> None:
    repository: MusicSingleReleaseRepository = InMemoryMusicSingleReleaseRepository()
    single = MusicSingleRelease(**EXAMPLE_SINGLE_DATA.copy())
    repository.create_single(single)
    assert repository.read_single(single.isrc) == single
    with pytest.raises(ValueError):
        repository.read_single("US0000000000")


def test_update_single() -> None:
    repository: MusicSingleReleaseRepository = InMemoryMusicSingleReleaseRepository()
    single: MusicSingleRelease = MusicSingleRelease(**EXAMPLE_SINGLE_DATA.copy())
    repository.create_single(single)
    updated_single: MusicSingleRelease = single.model_copy()
    updated_single.isrc = single.isrc
    updated_single.title = "Updated Title"
    repository.update_single(single.isrc, updated_single)
    assert repository.read_single(single.isrc) == updated_single


def test_update_single_not_found() -> None:
    repository: MusicSingleReleaseRepository = InMemoryMusicSingleReleaseRepository()
    single = MusicSingleRelease(**EXAMPLE_SINGLE_DATA.copy())
    with pytest.raises(ValueError, match=SINGLE_NOT_FOUND):
        repository.update_single("US1234567890", single)


def test_delete_single() -> None:
    repository: MusicSingleReleaseRepository = InMemoryMusicSingleReleaseRepository()
    single = MusicSingleRelease(**EXAMPLE_SINGLE_DATA.copy())
    repository.create_single(single)
    repository.delete_single(single.isrc)
    with pytest.raises(ValueError):
        repository.read_single(single.isrc)


def test_delete_single_not_found() -> None:
    repository: MusicSingleReleaseRepository = InMemoryMusicSingleReleaseRepository()
    with pytest.raises(ValueError, match=SINGLE_NOT_FOUND):
        repository.delete_single("US1234567890")
