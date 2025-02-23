from typing import List, Optional
from datetime import date, timedelta
import logging
import os
from pydantic import BaseModel, Field, HttpUrl


# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.WARNING),
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# FIXME: pydantic_core._pydantic_core.ValidationError: 1 validation error for Crew Value error, Please provide an
# OpenAI API key.
# Need to set false OPENAI_API_KEY to a non-empty string to avoid this error using memory=True on your Crew()
# if not os.environ.get("OPENAI_API_KEY"):
#     os.environ["OPENAI_API_KEY"] = "N/A"


class MusicSingleRelease(BaseModel):
    """
    Pydantic model representing a music single release.
    """

    title: str = Field(..., description="The title of the music single.")
    isrc: str = Field(
        ...,
        description="International Standard Recording Code (ISRC) - a 12-character unique identifier for the recording.",
        min_length=12,
        max_length=12,
        pattern=r"^[A-Z]{2}[A-Z0-9]{3}\d{7}$",  # Basic ISRC format validation
    )  # Basic ISRC format validation

    artist_names: List[str] = Field(
        ...,
        description="List of artist names for the single (e.g., ['Artist 1', 'Artist 2 ft. Guest']).",
        min_length=1,
    )
    release_date: date = Field(
        ..., description="The date the single was officially released."
    )
    genres: List[str] = Field(
        ...,
        description="List of genres associated with the single (e.g., ['Pop', 'Electronic', 'Indie Rock']).",
        min_length=1,
    )
    label: Optional[str] = Field(
        None, description="Optional: The record label releasing the single."
    )
    version: Optional[str] = Field(
        None,
        description="Optional: Version of the single (e.g., 'Radio Edit', 'Extended Mix', 'Acoustic').",
    )
    formats: Optional[List[str]] = Field(
        None,
        description="Optional: List of formats the single is released in (e.g., ['Digital', 'Vinyl', 'CD']).",
    )
    duration: Optional[timedelta] = Field(
        None,
        description="Optional: Duration of the single track.",
    )
    artwork_url: Optional[HttpUrl] = Field(
        None, description="Optional: URL to the artwork image for the single."
    )
    audio_preview_url: Optional[HttpUrl] = Field(
        None, description="Optional: URL to an audio preview or snippet of the single."
    )
    catalog_number: Optional[str] = Field(
        None, description="Optional: Catalog number assigned to the release."
    )
    subgenres: Optional[List[str]] = Field(
        None,
        description="Optional: List of subgenres for more specific categorization.",
    )
    composers: Optional[List[str]] = Field(
        None, description="Optional: List of composers who wrote the single."
    )
    producers: Optional[List[str]] = Field(
        None, description="Optional: List of producers who produced the single."
    )
    language: Optional[str] = Field(
        None,
        description="Optional: Language of the lyrics in the single, if applicable.",
    )
    lyrics: Optional[str] = Field(
        None, description="Optional: Full lyrics of the single."
    )
    notes: Optional[str] = Field(
        None,
        description="Optional: Any additional notes or information about the single.",
    )
