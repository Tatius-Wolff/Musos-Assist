import pytest
from musos_assist.domain.ports import MusicSingleReleaseRepository
from musos_assist.domain.models import MusicSingleRelease
from musos_assist.constants import EXAMPLE_SINGLE_DATA


class IncompleteMusicSingleReleaseRepository(MusicSingleReleaseRepository):
    pass


def test_create_single_raises_not_implemented_error() -> None:
    repository = IncompleteMusicSingleReleaseRepository()
    with pytest.raises(NotImplementedError):
        repository.create_single(MusicSingleRelease(**EXAMPLE_SINGLE_DATA.copy()))


def test_list_singles_raises_not_implemented_error() -> None:
    repository = IncompleteMusicSingleReleaseRepository()
    with pytest.raises(NotImplementedError):
        repository.list_singles()


def test_read_single_raises_not_implemented_error() -> None:
    repository = IncompleteMusicSingleReleaseRepository()
    with pytest.raises(NotImplementedError):
        repository.read_single("US1234567890")


def test_update_single_raises_not_implemented_error() -> None:
    repository = IncompleteMusicSingleReleaseRepository()
    with pytest.raises(NotImplementedError):
        repository.update_single(
            "US1234567890", MusicSingleRelease(**EXAMPLE_SINGLE_DATA.copy())
        )


def test_delete_single_raises_not_implemented_error() -> None:
    repository = IncompleteMusicSingleReleaseRepository()
    with pytest.raises(NotImplementedError):
        repository.delete_single("US1234567890")
