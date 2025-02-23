from typing import Any

SINGLE_NOT_FOUND = "Single not found"

EXAMPLE_SINGLE_DATA: dict[str, Any] = {
    "title": "My Awesome Song",
    "isrc": "USX9P2400001",
    "artist_names": ["My Band"],
    "release_date": "2024-01-15",
    "genres": ["Rock", "Indie"],
    "label": "Independent Label",
    "version": "Original",
    "formats": ["Digital", "Vinyl"],
    "duration": "PT3M45S",  # ISO 8601 duration format might be better in real-world, or seconds/minutes
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
