from typing import Optional, Any
import logging
import os
from pydantic import BaseModel, Field, ValidationInfo, field_validator

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.WARNING),
    format="%(asctime)s - %(levelname)s - %(message)s",
)

ABS_MAX_AGE: int = 150


class Gender(BaseModel):
    """
    This is an immutable object representing audience insights about audience gender

    Gender [male=89.2, female=9.2, other=1.6000061]
    """

    male: float = Field(description="Percentage of Male audience")
    female: float = Field(description="Percentage of Female audience")
    other: Optional[float] = Field(
        default=None, description="Percentage of non-Male and non-Female audience"
    )

    @field_validator("male", "female", "other")
    def validate_percentage(cls: "Gender", v: float, info: ValidationInfo) -> float:
        if v is not None and not 0.0 <= v <= 100.0:
            raise ValueError(
                f"Parameter [{info.field_name}]: [{v}] is not between [0.0] and [100.0]."
            )
        return v

    def model_post_init(self, __context__: Any) -> None:
        if self.other is None:
            self.other = round(100.0 - (self.male + self.female), 1)
        total = self.male + self.female + self.other
        if not 99.9 <= total <= 100.1:
            raise ValueError(
                f"Total percentage [{self.male}] + [{self.female}] + [{self.other}] does not equal 100%."
            )


class AgeRange(BaseModel):
    """
    This is an immutable object representing audience insights about audience age range

    AgeRange [min_age=18, max_age=24, percent=13.0]

    TODO this object needs to be the whole range
    """

    min_age: int = Field(description="The beginning of the audience age range")
    max_age: Optional[int] = Field(
        default=None, description="The end of the audience age range"
    )
    percent: float = Field(description="Percentage of the audience age range")

    @field_validator("min_age", "max_age")
    def validate_age(cls: "AgeRange", v: float, info: ValidationInfo) -> float:
        if v is not None and not 0 <= v <= ABS_MAX_AGE:
            raise ValueError(
                f"Parameter [{info.field_name}]: [{v}] is not between [0] and [{ABS_MAX_AGE}]."
            )
        return v

    @field_validator("percent")
    def validate_percentage(cls: "AgeRange", v: float, info: ValidationInfo) -> float:
        if not 0.0 <= v <= 100.0:
            raise ValueError(
                f"Parameter [percent]: [{v}] is not between [0.0] and [100.0]."
            )
        return v

    def model_post_init(self, __context__: Any) -> None:
        if self.max_age is None:
            self.max_age = ABS_MAX_AGE


class TopLocation(BaseModel):
    """
    This is an immutable object representing audience insights about audience top locations

    TopLocation [location=New South Wales, percent=43.4]

    TODO this object needs to be the whole range
    """

    location: str = Field(description="Name of location")
    percent: float = Field(description="Percentage of location")

    @field_validator("percent")
    def validate_percent(cls: "TopLocation", v: float) -> float:
        if not 0.0 <= v <= 100.0:
            raise ValueError(
                f"Parameter [percent]: [{v}] is not between [0.0] and [100.0]."
            )
        return v


class Audience(BaseModel):
    """
    This is an immutable object representing audience insights including gender, age range and top locations.
    """

    gender: Gender = Field(description="The audience gender statistics")
    agerange: list[AgeRange] = Field(description="An array of audience age ranges")
    toplocation: list[TopLocation] = Field(
        description="An array of the audience top locations"
    )
