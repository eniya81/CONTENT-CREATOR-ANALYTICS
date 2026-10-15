from typing import Optional

from sqlalchemy.orm import Session

from app.models.audience import Audience
from app.models.growth import Growth


SUPPORTED_PLATFORMS = {
    "youtube": "YouTube",
    "instagram": "Instagram",
    "tiktok": "TikTok",
    "facebook": "Facebook",
    "linkedin": "LinkedIn",
    "x": "X",
}


def normalize_platform(
    platform: Optional[str]
) -> Optional[str]:
    """
    Normalize platform names so API requests such as
    youtube, YouTube, YOUTUBE all map to YouTube.
    """

    if platform is None:
        return None

    cleaned = platform.strip()

    if not cleaned or cleaned.lower() == "all":
        return None

    return SUPPORTED_PLATFORMS.get(
        cleaned.lower(),
        cleaned
    )


# ==========================================================
# AUDIENCE RECORDS
# ==========================================================

def get_audience_records(
    db: Session,
    platform: Optional[str] = None,
    creator_id: Optional[int] = None
):
    query = db.query(Audience)

    if creator_id is not None:
        query = query.filter(
            Audience.creator_id == creator_id
        )

    normalized_platform = normalize_platform(platform)

    if normalized_platform is not None:
        query = query.filter(
            Audience.platform == normalized_platform
        )

    return query.all()


def get_total_followers(
    db: Session,
    platform: Optional[str] = None,
    creator_id: Optional[int] = None
):
    records = get_audience_records(
        db,
        platform,
        creator_id
    )

    return sum(
        record.followers
        for record in records
    )


def get_total_reach(
    db: Session,
    platform: Optional[str] = None,
    creator_id: Optional[int] = None
):
    records = get_audience_records(
        db,
        platform,
        creator_id
    )

    return sum(
        record.reach
        for record in records
    )


def get_total_impressions(
    db: Session,
    platform: Optional[str] = None,
    creator_id: Optional[int] = None
):
    records = get_audience_records(
        db,
        platform,
        creator_id
    )

    return sum(
        record.impressions
        for record in records
    )


def get_gender_distribution(
    db: Session,
    platform: Optional[str] = None,
    creator_id: Optional[int] = None
):
    records = get_audience_records(
        db,
        platform,
        creator_id
    )

    distribution = {}

    for record in records:
        gender = record.gender

        distribution[gender] = (
            distribution.get(gender, 0)
            + record.followers
        )

    return distribution


def get_age_distribution(
    db: Session,
    platform: Optional[str] = None,
    creator_id: Optional[int] = None
):
    records = get_audience_records(
        db,
        platform,
        creator_id
    )

    distribution = {}

    for record in records:
        age_group = record.age_group

        distribution[age_group] = (
            distribution.get(age_group, 0)
            + record.followers
        )

    return distribution


def get_top_countries(
    db: Session,
    platform: Optional[str] = None,
    limit: int = 5,
    creator_id: Optional[int] = None
):
    records = get_audience_records(
        db,
        platform,
        creator_id
    )

    country_data = {}

    for record in records:
        country = record.country

        country_data[country] = (
            country_data.get(country, 0)
            + record.followers
        )

    sorted_countries = sorted(
        country_data.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return [
        {
            "country": country,
            "followers": followers
        }
        for country, followers
        in sorted_countries[:limit]
    ]


def get_top_cities(
    db: Session,
    platform: Optional[str] = None,
    limit: int = 5,
    creator_id: Optional[int] = None
):
    records = get_audience_records(
        db,
        platform,
        creator_id
    )

    city_data = {}

    for record in records:
        city = record.city

        city_data[city] = (
            city_data.get(city, 0)
            + record.followers
        )

    sorted_cities = sorted(
        city_data.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return [
        {
            "city": city,
            "followers": followers
        }
        for city, followers
        in sorted_cities[:limit]
    ]


def get_device_distribution(
    db: Session,
    platform: Optional[str] = None,
    creator_id: Optional[int] = None
):
    records = get_audience_records(
        db,
        platform,
        creator_id
    )

    distribution = {}

    for record in records:
        device = record.device_type

        distribution[device] = (
            distribution.get(device, 0)
            + record.followers
        )

    return distribution


def get_audience_report(
    db: Session,
    platform: Optional[str] = None,
    creator_id: Optional[int] = None
):
    normalized_platform = normalize_platform(platform)

    records = get_audience_records(
        db,
        normalized_platform,
        creator_id
    )

    return {
        "platform": normalized_platform or "All Platforms",

        "total_followers": sum(
            record.followers
            for record in records
        ),

        "total_reach": sum(
            record.reach
            for record in records
        ),

        "total_impressions": sum(
            record.impressions
            for record in records
        ),

        "gender_distribution":
            get_gender_distribution(
                db,
                normalized_platform,
                creator_id
            ),

        "age_distribution":
            get_age_distribution(
                db,
                normalized_platform,
                creator_id
            ),

        "top_countries":
            get_top_countries(
                db,
                normalized_platform,
                5,
                creator_id
            ),

        "top_cities":
            get_top_cities(
                db,
                normalized_platform,
                5,
                creator_id
            ),

        "device_distribution":
            get_device_distribution(
                db,
                normalized_platform,
                creator_id
            )
    }


# ==========================================================
# GROWTH
# ==========================================================

def get_growth_records(
    db: Session,
    platform: Optional[str] = None,
    creator_id: Optional[int] = None
):
    """
    Fetch growth records.

    No platform:
        Returns creator-level NULL-platform records.

    Platform selected:
        Returns records belonging to that platform.

    When creator_id is supplied, only that creator's
    records are returned.
    """

    normalized_platform = normalize_platform(platform)

    query = db.query(Growth)

    if creator_id is not None:
        query = query.filter(
            Growth.creator_id == creator_id
        )

    if normalized_platform is not None:
        query = query.filter(
            Growth.platform == normalized_platform
        )
    else:
        query = query.filter(
            Growth.platform.is_(None)
        )

    return (
        query
        .order_by(
            Growth.date.asc(),
            Growth.id.asc()
        )
        .limit(30)
        .all()
    )


def get_growth_report(
    db: Session,
    platform: Optional[str] = None,
    creator_id: Optional[int] = None
):
    """
    Calculate follower growth and growth percentage.

    Platform-specific records are calculated independently
    for the selected platform.

    When creator_id is supplied, calculations are restricted
    to that creator.
    """

    growth_records = get_growth_records(
        db,
        platform,
        creator_id
    )

    result = []

    previous_followers = None

    for record in growth_records:

        if previous_followers is None:

            daily_growth = 0
            growth_percentage = 0

        else:

            daily_growth = (
                record.followers
                - previous_followers
            )

            if previous_followers == 0:

                growth_percentage = 0

            else:

                growth_percentage = (
                    daily_growth
                    / previous_followers
                ) * 100

        result.append({
            "date": record.date,
            "platform": record.platform,
            "followers": record.followers,
            "reach": record.reach,
            "engagement_rate": record.engagement_rate,
            "daily_growth": daily_growth,
            "growth_percentage": round(
                growth_percentage,
                2
            )
        })

        previous_followers = record.followers

    return result


# ==========================================================
# AUDIENCE TRENDS
# ==========================================================

def get_audience_trends(
    db: Session,
    platform: Optional[str] = None,
    creator_id: Optional[int] = None
):
    """
    Return historical audience/follower trends.

    All Platforms:
        Uses NULL-platform Growth records.

    Selected Platform:
        Uses that platform's Growth records.

    When creator_id is supplied, only that creator's
    records are returned.
    """

    growth_records = get_growth_records(
        db,
        platform,
        creator_id
    )

    return [
        {
            "date": record.date,
            "platform": record.platform,
            "followers": record.followers,
            "reach": record.reach
        }
        for record in growth_records
    ]