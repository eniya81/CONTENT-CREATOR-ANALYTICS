from typing import Optional

from pydantic import BaseModel, Field


SUPPORTED_PLATFORMS = {
    "youtube": "YouTube",
    "instagram": "Instagram",
    "tiktok": "TikTok",
    "facebook": "Facebook",
    "linkedin": "LinkedIn",
    "x": "X",
}


def normalize_platform(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None

    cleaned = value.strip()

    if not cleaned:
        return None

    return SUPPORTED_PLATFORMS.get(
        cleaned.lower(),
        cleaned
    )


class AudienceCreate(BaseModel):
    creator_id: int = Field(..., gt=0)

    platform: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    age_group: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    gender: str = Field(
        ...,
        min_length=1,
        max_length=20
    )

    country: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    city: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    device_type: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    active_hour: int = Field(
        ...,
        ge=0,
        le=23
    )

    followers: int = Field(
        default=0,
        ge=0
    )

    impressions: int = Field(
        default=0,
        ge=0
    )

    reach: int = Field(
        default=0,
        ge=0
    )


class AudienceUpdate(BaseModel):
    creator_id: Optional[int] = Field(
        default=None,
        gt=0
    )

    platform: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    age_group: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    gender: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=20
    )

    country: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    city: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    device_type: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    active_hour: Optional[int] = Field(
        default=None,
        ge=0,
        le=23
    )

    followers: Optional[int] = Field(
        default=None,
        ge=0
    )

    impressions: Optional[int] = Field(
        default=None,
        ge=0
    )

    reach: Optional[int] = Field(
        default=None,
        ge=0
    )