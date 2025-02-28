import pytest
from pydantic import ValidationError
from datetime import date, timedelta
from musos_assist.domain.models import MusicSingleRelease


# Valid data for testing
VALID_SINGLE_DATA = {
    "title": "Example Song Title",
    "isrc": "USX9P2312345",
    "artist_names": ["Example Artist"],
    "release_date": date(2023, 10, 27),
    "genres": ["Pop"],
    "label": "Example Records",
    "version": "Radio Edit",
    "formats": ["Digital"],
    "duration": timedelta(minutes=3, seconds=30),
    "artwork_url": "https://example.com/artwork.jpg",
    "audio_preview_url": "https://example.com/preview.mp3",
    "catalog_number": "ER12345",
    "subgenres": ["Synth-pop"],
    "composers": ["John Doe", "Jane Smith"],
    "producers": ["Producer X"],
    "language": "English",
    "lyrics": "Lyrics go here,\nThis is my song,\nThis is a cool song.",
    "notes": "This is a radio edit version.",
}


def test_valid_music_single_release() -> None:
    """Test creating a valid MusicSingleRelease model."""
    single = MusicSingleRelease(**VALID_SINGLE_DATA.copy())  # type: ignore[arg-type]
    assert isinstance(single, MusicSingleRelease)
    assert single.title == VALID_SINGLE_DATA["title"]
    assert single.isrc == VALID_SINGLE_DATA["isrc"]
    assert single.artist_names == VALID_SINGLE_DATA["artist_names"]
    assert single.release_date == VALID_SINGLE_DATA["release_date"]
    assert single.genres == VALID_SINGLE_DATA["genres"]
    assert single.label == VALID_SINGLE_DATA["label"]
    assert single.version == VALID_SINGLE_DATA["version"]
    assert single.formats == VALID_SINGLE_DATA["formats"]
    assert single.duration == VALID_SINGLE_DATA["duration"]
    assert (
        str(single.artwork_url) == VALID_SINGLE_DATA["artwork_url"]
    )  # Convert HttpUrl to string for comparison
    assert (
        str(single.audio_preview_url) == VALID_SINGLE_DATA["audio_preview_url"]
    )  # Convert HttpUrl to string for comparison
    assert single.catalog_number == VALID_SINGLE_DATA["catalog_number"]
    assert single.subgenres == VALID_SINGLE_DATA["subgenres"]
    assert single.composers == VALID_SINGLE_DATA["composers"]
    assert single.producers == VALID_SINGLE_DATA["producers"]
    assert single.language == VALID_SINGLE_DATA["language"]
    assert single.lyrics == VALID_SINGLE_DATA["lyrics"]
    assert single.notes == VALID_SINGLE_DATA["notes"]


def test_missing_required_fields() -> None:
    """Test validation error when required fields are missing."""
    required_fields = ["title", "isrc", "artist_names", "release_date", "genres"]
    for field in required_fields:
        invalid_data = VALID_SINGLE_DATA.copy()
        del invalid_data[field]
        with pytest.raises(ValidationError) as excinfo:
            MusicSingleRelease(**invalid_data)  # type: ignore[arg-type]
        assert field in str(
            excinfo.value
        ), f"ValidationError should mention missing field: {field}"


def test_invalid_isrc_format() -> None:
    """Test validation error for invalid ISRC formats."""
    invalid_isrcs = [
        "USX9P231234",  # Too short
        "USX9P23123456",  # Too long
        "USX9P231234!",  # Invalid character
        "usx9p2312345",  # Lowercase country code
        "1SX9P2312345",  # Digit as first country code
    ]
    for invalid_isrc in invalid_isrcs:
        invalid_data = VALID_SINGLE_DATA.copy()
        invalid_data["isrc"] = invalid_isrc
        with pytest.raises(ValidationError) as excinfo:
            MusicSingleRelease(**invalid_data)  # type: ignore[arg-type]
        assert "isrc" in str(
            excinfo.value
        ), f"ValidationError for invalid ISRC: {invalid_isrc}"


def test_invalid_release_date_type() -> None:
    """Test validation error for invalid release_date type."""
    invalid_data = VALID_SINGLE_DATA.copy()
    invalid_data["release_date"] = "20231027"  # String instead of date
    with pytest.raises(ValidationError) as excinfo:
        MusicSingleRelease(**invalid_data)  # type: ignore[arg-type]
    assert "release_date" in str(excinfo.value)


def test_invalid_artwork_url_format() -> None:
    """Test validation error for invalid artwork_url format."""
    invalid_urls = [
        "not a url",
        "ftp://example.com/artwork.jpg",  # Not http/https
        "http://",  # Incomplete URL
    ]
    for invalid_url in invalid_urls:
        invalid_data = VALID_SINGLE_DATA.copy()
        invalid_data["artwork_url"] = invalid_url
        with pytest.raises(ValidationError) as excinfo:
            MusicSingleRelease(**invalid_data)  # type: ignore[arg-type]
        assert "artwork_url" in str(
            excinfo.value
        ), f"ValidationError for invalid artwork_url: {invalid_url}"


def test_invalid_audio_preview_url_format() -> None:
    """Test validation error for invalid audio_preview_url format."""
    invalid_urls = [
        "not a url",
        "ftp://example.com/preview.mp3",  # Not http/https
        "http://",  # Incomplete URL
    ]
    for invalid_url in invalid_urls:
        invalid_data = VALID_SINGLE_DATA.copy()
        invalid_data["audio_preview_url"] = invalid_url
        with pytest.raises(ValidationError) as excinfo:
            MusicSingleRelease(**invalid_data)  # type: ignore[arg-type]
        assert "audio_preview_url" in str(
            excinfo.value
        ), f"ValidationError for invalid audio_preview_url: {invalid_url}"


def test_optional_fields_can_be_none() -> None:
    """Test that optional fields can be set to None."""
    optional_fields = [
        "label",
        "version",
        "formats",
        "duration",
        "artwork_url",
        "audio_preview_url",
        "catalog_number",
        "subgenres",
        "composers",
        "producers",
        "language",
        "lyrics",
        "notes",
    ]
    for field in optional_fields:
        valid_data_with_optional_none = VALID_SINGLE_DATA.copy()
        valid_data_with_optional_none[field] = None
        single = MusicSingleRelease(**valid_data_with_optional_none)  # type: ignore[arg-type]
        assert (
            getattr(single, field) is None
        ), f"Optional field '{field}' should accept None"


def test_empty_artist_names_list() -> None:
    """Test validation error when artist_names list is empty."""
    invalid_data = VALID_SINGLE_DATA.copy()
    invalid_data["artist_names"] = []
    with pytest.raises(ValidationError) as excinfo:
        MusicSingleRelease(**invalid_data)  # type: ignore[arg-type]
    assert "artist_names" in str(excinfo.value)


def test_empty_genres_list() -> None:
    """Test validation error when genres list is empty."""
    invalid_data = VALID_SINGLE_DATA.copy()
    invalid_data["genres"] = []
    with pytest.raises(ValidationError) as excinfo:
        MusicSingleRelease(**invalid_data)  # type: ignore[arg-type]
    assert "genres" in str(excinfo.value)
