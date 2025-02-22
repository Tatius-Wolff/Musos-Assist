from datetime import date
import logging
import os
from pydantic import BaseModel, Field, EmailStr, HttpUrl

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.WARNING),
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class MarketingContact(BaseModel):
    """
    This is an immutable object representing a marketing contact.

    Attributes:
        organisation (str): The name of the organisation.
        name (str): The name of the contact person.
        email (EmailStr): The email address of the contact person.
    """

    organisation: str = Field(description="The name of the organisation.", min_length=1)
    name: str = Field(description="The name of the contact person.", min_length=1)
    email: EmailStr = Field(description="The email address of the contact person.")


class PressCoverage(BaseModel):
    """
    This is an immutable object representing press coverage.

    Attributes:
        subject (str): The subject of the press coverage. Must be at least 1 character long.
        publish_date (date): The date the press coverage was published.
        web_link (HttpUrl): The URL of the press coverage. Must be at least 1 character long.
        body (str): The body of the press coverage. Must be at least 1 character long. Assumed to be HTML content as a string.
        images (list[str]): The images of the press coverage. Assumed to be image URLs as strings.
        author (str): The author of the press coverage. Must be at least 1 character long.
        marketing_contact (MarketingContact): The marketing contact for the press coverage.
    """

    subject: str = Field(description="The subject of the press coverage.", min_length=1)
    publish_date: date = Field(description="The date the press coverage was published.")
    web_link: HttpUrl = Field(
        description="The URL of the press coverage.", min_length=1
    )
    body: str = Field(
        description="The body of the press coverage.", min_length=1
    )  # Assuming HTML content as a string
    images: list[str] = Field(
        description="The images of the press coverage."
    )  # Assuming image URLs as strings
    author: str = Field(description="The author of the press coverage.", min_length=1)
    marketing_contact: MarketingContact = Field(
        description="The marketing contact for the press coverage."
    )


class PressKit(BaseModel):
    """
    This is an immutable object representing a press kit.

    Attributes:
        presscoverage (PressCoverage): The press coverage to be added to the press kit.
    """

    presscoverage: PressCoverage = Field(
        description="The press coverage to be added to the press kit."
    )
