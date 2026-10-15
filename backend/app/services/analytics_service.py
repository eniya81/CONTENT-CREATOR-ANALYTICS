from typing import Optional

from sqlalchemy.orm import Session

from app.models.content import Content
from app.models.audience import Audience
from app.models.growth import Growth


# ---------------------------------------------------------
# COMMON CONTENT QUERY
# ---------------------------------------------------------

def _get_contents(
    db: Session,
    platform: Optional[str] = None,
    creator_id: Optional[int] = None
):
    """
    Fetch content records.

    platform=None or platform="All" -> all platforms
    otherwise -> case-insensitive platform filter

    creator_id supplied -> only that creator's content
    """

    query = db.query(Content)

    if creator_id is not None:
        query = query.filter(
            Content.creator_id == creator_id
        )

    if platform and platform.strip().lower() != "all":
        query = query.filter(
            Content.platform.ilike(
                platform.strip()
            )
        )

    return query.all()


# ---------------------------------------------------------
# ENGAGEMENT CALCULATION
# ---------------------------------------------------------

def calculate_engagement_rate(content):
    """
    Calculate total engagement and engagement rate.

    Engagement rate =
        (likes + comments + shares + saves) / reach * 100

    If reach is zero, engagement rate is zero.
    """

    total_engagement = (
        (content.likes or 0)
        + (content.comments or 0)
        + (content.shares or 0)
        + (content.saves or 0)
    )

    reach = content.reach or 0

    if reach == 0:
        engagement_rate = 0
    else:
        engagement_rate = (
            total_engagement / reach
        ) * 100

    return total_engagement, round(
        engagement_rate,
        2
    )


# ---------------------------------------------------------
# SINGLE CONTENT ENGAGEMENT
# ---------------------------------------------------------

def get_content_engagement(
    db: Session,
    content_id: int,
    creator_id: Optional[int] = None
):
    """
    Get engagement analytics for a single content item.
    """

    query = (
        db.query(Content)
        .filter(
            Content.id == content_id
        )
    )

    if creator_id is not None:
        query = query.filter(
            Content.creator_id == creator_id
        )

    content = query.first()

    if not content:
        return None

    total_engagement, engagement_rate = (
        calculate_engagement_rate(content)
    )

    return {
        "content_id": content.id,
        "platform": content.platform,
        "views": content.views,
        "reach": content.reach,
        "total_engagement": total_engagement,
        "engagement_rate": engagement_rate
    }


# ---------------------------------------------------------
# TOP CONTENT
# ---------------------------------------------------------

def get_top_content(
    db: Session,
    platform: Optional[str] = None,
    creator_id: Optional[int] = None
):
    """
    Get top-performing content.

    If a platform is selected, only that platform's
    content is considered.

    If creator_id is supplied, only that creator's
    content is considered.
    """

    contents = _get_contents(
        db,
        platform,
        creator_id
    )

    analytics = []

    for content in contents:

        _, engagement_rate = (
            calculate_engagement_rate(content)
        )

        analytics.append({
            "content_id": content.id,
            "content_title": content.content_title,
            "platform": content.platform,
            "views": content.views,
            "reach": content.reach,
            "watch_time": content.watch_time,
            "engagement_rate": engagement_rate
        })

    analytics.sort(
        key=lambda item: item["engagement_rate"],
        reverse=True
    )

    return analytics[:5]


# ---------------------------------------------------------
# PLATFORM PERFORMANCE
# ---------------------------------------------------------

def get_platform_performance(
    db: Session,
    platform: Optional[str] = None,
    creator_id: Optional[int] = None
):
    """
    Calculate performance metrics for platforms.

    If a platform is selected, only that platform's
    records are considered.

    If creator_id is supplied, only that creator's
    content is considered.
    """

    contents = _get_contents(
        db,
        platform,
        creator_id
    )

    platform_data = {}

    for content in contents:

        _, engagement_rate = (
            calculate_engagement_rate(content)
        )

        platform_name = content.platform

        if platform_name not in platform_data:
            platform_data[platform_name] = {
                "total_views": 0,
                "total_likes": 0,
                "total_comments": 0,
                "total_reach": 0,
                "engagement_rates": []
            }

        platform_data[platform_name][
            "total_views"
        ] += content.views or 0

        platform_data[platform_name][
            "total_likes"
        ] += content.likes or 0

        platform_data[platform_name][
            "total_comments"
        ] += content.comments or 0

        platform_data[platform_name][
            "total_reach"
        ] += content.reach or 0

        platform_data[platform_name][
            "engagement_rates"
        ].append(
            engagement_rate
        )

    result = []

    for platform_name, data in platform_data.items():

        if data["engagement_rates"]:
            average_engagement_rate = (
                sum(data["engagement_rates"])
                / len(data["engagement_rates"])
            )
        else:
            average_engagement_rate = 0

        result.append({
            "platform": platform_name,
            "total_views": data["total_views"],
            "total_likes": data["total_likes"],
            "total_comments": data["total_comments"],
            "total_reach": data["total_reach"],
            "average_engagement_rate": round(
                average_engagement_rate,
                2
            )
        })

    result.sort(
        key=lambda item: item[
            "average_engagement_rate"
        ],
        reverse=True
    )

    return result


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

def get_summary(
    db: Session,
    platform: Optional[str] = None,
    creator_id: Optional[int] = None
):
    """
    Generate analytics summary.

    Content metrics respect the selected platform.

    Audience and growth values are restricted to the
    supplied creator when creator_id is provided.
    """

    contents = _get_contents(
        db,
        platform,
        creator_id
    )

    audience_query = db.query(Audience)

    growth_query = db.query(Growth)

    if creator_id is not None:
        audience_query = audience_query.filter(
            Audience.creator_id == creator_id
        )

        growth_query = growth_query.filter(
            Growth.creator_id == creator_id
        )

    audiences = audience_query.all()

    # Preserve the existing summary behavior:
    # selected platform uses its platform-specific growth
    # records; All Platforms uses creator-level NULL-platform
    # growth records.
    if platform and platform.strip().lower() != "all":
        growth_query = growth_query.filter(
            Growth.platform.ilike(
                platform.strip()
            )
        )
    else:
        growth_query = growth_query.filter(
            Growth.platform.is_(None)
        )

    growth_records = growth_query.all()

    total_content = len(contents)

    total_views = sum(
        content.views or 0
        for content in contents
    )

    total_likes = sum(
        content.likes or 0
        for content in contents
    )

    total_comments = sum(
        content.comments or 0
        for content in contents
    )

    total_shares = sum(
        content.shares or 0
        for content in contents
    )

    total_reach = sum(
        content.reach or 0
        for content in contents
    )

    total_followers = sum(
        audience.followers or 0
        for audience in audiences
    )

    # -----------------------------------------------------
    # Engagement
    # -----------------------------------------------------

    engagement_rates = []

    for content in contents:

        _, engagement_rate = (
            calculate_engagement_rate(content)
        )

        engagement_rates.append(
            engagement_rate
        )

    if engagement_rates:

        average_engagement_rate = (
            sum(engagement_rates)
            / len(engagement_rates)
        )

    elif growth_records:

        average_engagement_rate = (
            sum(
                record.engagement_rate or 0
                for record in growth_records
            )
            / len(growth_records)
        )

    else:

        average_engagement_rate = 0

    # -----------------------------------------------------
    # Best Platform
    # -----------------------------------------------------

    platform_performance = (
        get_platform_performance(
            db,
            platform,
            creator_id
        )
    )

    if platform_performance:

        best_platform = (
            platform_performance[0]["platform"]
        )

    else:

        best_platform = None

    # -----------------------------------------------------
    # Top Content
    # -----------------------------------------------------

    top_content = get_top_content(
        db,
        platform,
        creator_id
    )

    if top_content:

        top_content_title = (
            top_content[0]["content_title"]
        )

    else:

        top_content_title = None

    # -----------------------------------------------------
    # Growth Percentage
    # -----------------------------------------------------

    growth_percentage = 0.0

    if len(growth_records) >= 2:

        ordered_growth = sorted(
            growth_records,
            key=lambda record: (
                record.date,
                record.id
            )
        )

        first_followers = (
            ordered_growth[0].followers or 0
        )

        latest_followers = (
            ordered_growth[-1].followers or 0
        )

        if first_followers != 0:

            growth_percentage = (
                (
                    latest_followers
                    - first_followers
                )
                / first_followers
            ) * 100

    return {
        "total_content": total_content,
        "total_views": total_views,
        "total_likes": total_likes,
        "total_comments": total_comments,
        "total_shares": total_shares,
        "total_reach": total_reach,
        "total_followers": total_followers,
        "average_engagement_rate": round(
            average_engagement_rate,
            2
        ),
        "growth_percentage": round(
            growth_percentage,
            2
        ),
        "best_platform": best_platform,
        "top_content": top_content_title
    }


# ---------------------------------------------------------
# ENGAGEMENT CHART
# ---------------------------------------------------------

def get_engagement_chart(
    db: Session,
    platform: Optional[str] = None,
    creator_id: Optional[int] = None
):
    """
    Generate engagement chart data.

    All Platforms:
        Uses creator-level Growth records.

    Specific platform:
        Uses Content records belonging to that
        creator and platform.
    """

    # -----------------------------------------------------
    # ALL PLATFORMS
    # -----------------------------------------------------

    if (
        platform is None
        or platform.strip().lower() == "all"
    ):

        query = db.query(Growth)

        if creator_id is not None:
            query = query.filter(
                Growth.creator_id == creator_id
            )

        query = query.filter(
            Growth.platform.is_(None)
        )

        growth_records = (
            query
            .order_by(
                Growth.date.asc(),
                Growth.id.asc()
            )
            .all()
        )

        return {
            "labels": [
                record.date.isoformat()
                for record in growth_records
                if record.date is not None
            ],
            "values": [
                round(
                    record.engagement_rate or 0,
                    2
                )
                for record in growth_records
                if record.date is not None
            ]
        }

    # -----------------------------------------------------
    # SPECIFIC PLATFORM
    # -----------------------------------------------------

    query = db.query(Content).filter(
        Content.platform.ilike(
            platform.strip()
        )
    )

    if creator_id is not None:
        query = query.filter(
            Content.creator_id == creator_id
        )

    contents = (
        query
        .order_by(
            Content.published_date.asc()
        )
        .all()
    )

    daily_data = {}

    for content in contents:

        if content.published_date is None:
            continue

        date_key = (
            content.published_date.isoformat()
        )

        _, engagement_rate = (
            calculate_engagement_rate(content)
        )

        if date_key not in daily_data:
            daily_data[date_key] = []

        daily_data[date_key].append(
            engagement_rate
        )

    labels = []
    values = []

    for date_key in sorted(
        daily_data.keys()
    ):

        rates = daily_data[date_key]

        average_rate = (
            sum(rates) / len(rates)
            if rates
            else 0
        )

        labels.append(date_key)

        values.append(
            round(
                average_rate,
                2
            )
        )

    return {
        "labels": labels,
        "values": values
    }


# ---------------------------------------------------------
# FOLLOWER CHART
# ---------------------------------------------------------

def get_follower_chart(
    db: Session,
    platform: Optional[str] = None,
    creator_id: Optional[int] = None
):
    """
    Generate follower growth chart data.

    platform=None or platform="All":
        Uses creator-level NULL-platform Growth records.

    Specific platform:
        Uses only that platform's Growth records.
    """

    query = db.query(Growth)

    if creator_id is not None:
        query = query.filter(
            Growth.creator_id == creator_id
        )

    if platform and platform.strip().lower() != "all":

        query = query.filter(
            Growth.platform.ilike(
                platform.strip()
            )
        )

    else:

        query = query.filter(
            Growth.platform.is_(None)
        )

    growth_records = (
        query
        .order_by(
            Growth.date.asc(),
            Growth.id.asc()
        )
        .all()
    )

    return {
        "labels": [
            record.date.isoformat()
            for record in growth_records
            if record.date is not None
        ],
        "values": [
            record.followers or 0
            for record in growth_records
            if record.date is not None
        ]
    }


# ---------------------------------------------------------
# PLATFORM COMPARISON
# ---------------------------------------------------------

def get_platform_comparison(
    db: Session,
    creator_id: Optional[int] = None
):
    """
    Compare all available platforms.

    Metrics:
        - Views
        - Reach
        - Likes
        - Comments
        - Engagement Rate
        - Growth

    Content metrics come from the Content table.

    Growth is calculated from the earliest and latest
    follower records for each platform in the Growth table.

    No analytics values are hard-coded.

    If creator_id is supplied, only that creator's data
    is considered.
    """

    # -----------------------------------------------------
    # CONTENT DATA
    # -----------------------------------------------------

    content_query = db.query(Content)

    if creator_id is not None:
        content_query = content_query.filter(
            Content.creator_id == creator_id
        )

    contents = content_query.all()

    platform_data = {}

    for content in contents:

        _, engagement_rate = (
            calculate_engagement_rate(content)
        )

        platform_name = (
            content.platform.strip()
        )

        if platform_name not in platform_data:

            platform_data[platform_name] = {
                "views": 0,
                "reach": 0,
                "likes": 0,
                "comments": 0,
                "engagement_rates": []
            }

        platform_data[platform_name][
            "views"
        ] += content.views or 0

        platform_data[platform_name][
            "reach"
        ] += content.reach or 0

        platform_data[platform_name][
            "likes"
        ] += content.likes or 0

        platform_data[platform_name][
            "comments"
        ] += content.comments or 0

        platform_data[platform_name][
            "engagement_rates"
        ].append(
            engagement_rate
        )

    # -----------------------------------------------------
    # GROWTH DATA
    # -----------------------------------------------------

    growth_query = db.query(Growth).filter(
        Growth.platform.isnot(None)
    )

    if creator_id is not None:
        growth_query = growth_query.filter(
            Growth.creator_id == creator_id
        )

    growth_records = (
        growth_query
        .order_by(
            Growth.platform.asc(),
            Growth.date.asc(),
            Growth.id.asc()
        )
        .all()
    )

    growth_by_platform = {}

    for record in growth_records:

        platform_name = (
            record.platform.strip()
        )

        platform_key = (
            platform_name.lower()
        )

        if platform_key not in growth_by_platform:
            growth_by_platform[
                platform_key
            ] = []

        growth_by_platform[
            platform_key
        ].append(record)

    # -----------------------------------------------------
    # CALCULATE PLATFORM GROWTH
    # -----------------------------------------------------

    platform_growth = {}

    for platform_key, records in (
        growth_by_platform.items()
    ):

        if len(records) < 2:

            platform_growth[
                platform_key
            ] = None

            continue

        first_followers = (
            records[0].followers or 0
        )

        latest_followers = (
            records[-1].followers or 0
        )

        if first_followers == 0:

            platform_growth[
                platform_key
            ] = None

            continue

        growth_percentage = (
            (
                latest_followers
                - first_followers
            )
            / first_followers
        ) * 100

        platform_growth[
            platform_key
        ] = round(
            growth_percentage,
            2
        )

    # -----------------------------------------------------
    # BUILD FINAL RESULT
    # -----------------------------------------------------

    result = {}

    for platform_name, data in (
        platform_data.items()
    ):

        engagement_rates = (
            data["engagement_rates"]
        )

        if engagement_rates:

            average_engagement_rate = (
                sum(engagement_rates)
                / len(engagement_rates)
            )

        else:

            average_engagement_rate = 0

        platform_key = (
            platform_name.lower()
        )

        result[platform_name] = {
            "views": data["views"],
            "reach": data["reach"],
            "engagement_rate": round(
                average_engagement_rate,
                2
            ),
            "likes": data["likes"],
            "comments": data["comments"],
            "growth": platform_growth.get(
                platform_key
            )
        }

    return result