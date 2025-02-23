from typing import Any
from httpx._models import Response
from fastapi.testclient import TestClient

from musos_assist.musicsinglerelease_api import app

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
    "notes": "Debut single.",
}

client = TestClient(app)  # Create a TestClient instance for your FastAPI app


def test_list_singles_empty() -> None:
    """Test listing singles when no singles exist."""
    response: Response = client.get("/singles/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_single_valid() -> None:
    """Test creating a valid music single."""
    response = client.post("/singles/", json=EXAMPLE_SINGLE_DATA)
    assert response.status_code == 201
    created_single = response.json()
    assert created_single["isrc"] == EXAMPLE_SINGLE_DATA["isrc"]
    assert created_single["title"] == EXAMPLE_SINGLE_DATA["title"]
    # ... (assert other fields as needed)


def test_create_single_isrc_exists() -> None:
    """Test creating a single with an ISRC that already exists."""
    # First, create a single to make the ISRC exist
    client.post("/singles/", json=EXAMPLE_SINGLE_DATA)
    # Then, try to create another with the same ISRC
    response = client.post("/singles/", json=EXAMPLE_SINGLE_DATA)
    assert response.status_code == 400
    assert response.json() == {"detail": "ISRC already exists"}


def test_create_single_invalid_data() -> None:
    """Test creating a single with invalid data (missing required field)."""
    invalid_data = EXAMPLE_SINGLE_DATA.copy()
    del invalid_data["title"]  # Remove required 'title' field
    response = client.post("/singles/", json=invalid_data)
    assert response.status_code == 422  # Unprocessable Entity for validation errors
    assert (
        "title" in response.json()["detail"][0]["loc"]
    )  # Check if the error is related to 'title' field


def test_read_single_exists() -> None:
    """Test reading an existing music single."""
    # First, create a single
    client.post("/singles/", json=EXAMPLE_SINGLE_DATA)
    # Then, read it
    response = client.get(f"/singles/{EXAMPLE_SINGLE_DATA['isrc']}")
    assert response.status_code == 200
    single = response.json()
    assert single["isrc"] == EXAMPLE_SINGLE_DATA["isrc"]
    assert single["title"] == EXAMPLE_SINGLE_DATA["title"]


def test_read_single_not_found() -> None:
    """Test reading a non-existent music single."""
    response = client.get("/singles/NONEXISTENT_ISRC")
    assert response.status_code == 404
    assert response.json() == {"detail": "Single not found"}


def test_list_singles_multiple() -> None:
    """Test listing singles when multiple singles exist."""
    single_data_1 = EXAMPLE_SINGLE_DATA.copy()
    single_data_1["isrc"] = "USX9P2400001"
    client.post("/singles/", json=single_data_1)
    single_data_2 = EXAMPLE_SINGLE_DATA.copy()
    single_data_2["isrc"] = "USX9P2400002"
    single_data_2["title"] = "Another Song"
    client.post("/singles/", json=single_data_2)

    response: Response = client.get("/singles/")
    assert response.status_code == 200
    singles_list = response.json()
    assert len(singles_list) >= 2  # Should have at least 2 singles
    isrcs_in_list = [single["isrc"] for single in singles_list]
    assert single_data_1["isrc"] in isrcs_in_list
    assert single_data_2["isrc"] in isrcs_in_list


def test_update_single_exists() -> None:
    """Test updating an existing music single."""
    # First, create a single
    client.post("/singles/", json=EXAMPLE_SINGLE_DATA)
    # Then, update it
    updated_data = EXAMPLE_SINGLE_DATA.copy()
    updated_data["title"] = "Updated Song Title"
    updated_data["label"] = "Updated Label"
    response = client.put(f"/singles/{EXAMPLE_SINGLE_DATA['isrc']}", json=updated_data)
    assert response.status_code == 200
    updated_single = response.json()
    assert updated_single["isrc"] == EXAMPLE_SINGLE_DATA["isrc"]
    assert updated_single["title"] == "Updated Song Title"
    assert updated_single["label"] == "Updated Label"


def test_update_single_not_found() -> None:
    """Test updating a non-existent music single."""
    updated_data = EXAMPLE_SINGLE_DATA.copy()
    updated_data["title"] = "Updated Song Title"
    updated_data["isrc"] = "USX9P2400003"  # ISRC in body is different from path
    response: Response = client.put(
        f"/singles/{updated_data['isrc']}", json=updated_data
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Single not found"}


def test_update_single_isrc_mismatch() -> None:
    """Test updating with ISRC mismatch in path and body."""
    # First, create a single
    client.post("/singles/", json=EXAMPLE_SINGLE_DATA)
    updated_data: dict[str, Any] = EXAMPLE_SINGLE_DATA.copy()
    updated_data["isrc"] = "USX9P2400004"  # ISRC in body is different from path
    response = client.put(f"/singles/{EXAMPLE_SINGLE_DATA['isrc']}", json=updated_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "ISRC in path and request body do not match"}


def test_delete_single_exists() -> None:
    """Test deleting an existing music single."""
    # First, create a single
    client.post("/singles/", json=EXAMPLE_SINGLE_DATA)
    # Then, delete it
    response = client.delete(f"/singles/{EXAMPLE_SINGLE_DATA['isrc']}")
    assert response.status_code == 204
    # Try to read it again, should be 404
    response_get_deleted = client.get(f"/singles/{EXAMPLE_SINGLE_DATA['isrc']}")
    assert response_get_deleted.status_code == 404


def test_delete_single_not_found() -> None:
    """Test deleting a non-existent music single."""
    response = client.delete("/singles/NONEXISTENT_ISRC")
    assert response.status_code == 404
    assert response.json() == {"detail": "Single not found"}
