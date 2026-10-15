from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.auth import get_current_user
from app.models.user import User

from app.services.analytics_service import (
    get_content_engagement,
    get_top_content,
    get_platform_performance,
    get_summary,
    get_engagement_chart,
    get_follower_chart,
    get_platform_comparison
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


# ---------------------------------------------------------
# SINGLE CONTENT ENGAGEMENT
# ---------------------------------------------------------

@router.get("/content/{content_id}/engagement")
def content_engagement(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = get_content_engagement(
        db,
        content_id,
        current_user.id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Content not found"
        )

    return {
        "message": "Engagement analytics fetched successfully",
        "data": result
    }


# ---------------------------------------------------------
# TOP CONTENT
# ---------------------------------------------------------

@router.get("/top-content")
def top_content(
    platform: Optional[str] = Query(
        default=None,
        description="Filter by platform. Use All or omit the parameter for all platforms."
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = get_top_content(
        db,
        platform,
        current_user.id
    )

    return {
        "message": "Top-performing content fetched successfully",
        "data": result
    }


# ---------------------------------------------------------
# PLATFORM PERFORMANCE
# ---------------------------------------------------------

@router.get("/platform-performance")
def platform_performance(
    platform: Optional[str] = Query(
        default=None,
        description="Filter by platform. Use All or omit the parameter for all platforms."
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = get_platform_performance(
        db,
        platform,
        current_user.id
    )

    return {
        "message": "Platform performance fetched successfully",
        "data": result
    }


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

@router.get("/summary")
def analytics_summary(
    platform: Optional[str] = Query(
        default=None,
        description="Filter content analytics by platform. Use All or omit for all platforms."
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = get_summary(
        db,
        platform,
        current_user.id
    )

    return {
        "message": "Analytics summary fetched successfully",
        "data": result
    }


# ---------------------------------------------------------
# ENGAGEMENT CHART
# ---------------------------------------------------------

@router.get("/chart/engagement")
def engagement_chart(
    platform: Optional[str] = Query(
        default=None,
        description="Filter engagement trend by platform."
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = get_engagement_chart(
        db,
        platform,
        current_user.id
    )

    return {
        "message": "Engagement chart data fetched successfully",
        "data": result
    }


# ---------------------------------------------------------
# FOLLOWER CHART
# ---------------------------------------------------------

@router.get("/chart/followers")
def follower_chart(
    platform: Optional[str] = Query(
        default=None,
        description="Filter follower growth by platform. Use All or omit for all platforms."
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = get_follower_chart(
        db,
        platform,
        current_user.id
    )

    return {
        "message": "Follower growth chart data fetched successfully",
        "data": result
    }


# ---------------------------------------------------------
# PLATFORM COMPARISON
# ---------------------------------------------------------

@router.get("/platform-comparison")
def platform_comparison(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = get_platform_comparison(
        db,
        current_user.id
    )

    return {
        "message": "Platform comparison fetched successfully",
        "data": result
    }