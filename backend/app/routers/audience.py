from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.audience import Audience
from app.schemas.audience import (
    AudienceCreate,
    AudienceUpdate
)
from app.services.audience_service import (
    get_audience_report,
    get_audience_trends,
    get_growth_report,
)


# =========================================================
# AUDIENCE CRUD ROUTER
# =========================================================

router = APIRouter(
    prefix="/audience",
    tags=["Audience"]
)


def verify_creator_access(
    creator_id: int,
    current_user: User
):
    if current_user.id != creator_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own audience data"
        )


def audience_to_dict(record: Audience):
    return {
        "id": record.id,
        "creator_id": record.creator_id,
        "platform": record.platform,
        "age_group": record.age_group,
        "gender": record.gender,
        "country": record.country,
        "city": record.city,
        "device_type": record.device_type,
        "active_hour": record.active_hour,
        "followers": record.followers,
        "impressions": record.impressions,
        "reach": record.reach
    }


# =========================================================
# CREATE AUDIENCE
# =========================================================

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def create_audience(
    audience: AudienceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_creator_access(
        audience.creator_id,
        current_user
    )

    new_audience = Audience(
        creator_id=audience.creator_id,
        platform=audience.platform,
        age_group=audience.age_group,
        gender=audience.gender,
        country=audience.country,
        city=audience.city,
        device_type=audience.device_type,
        active_hour=audience.active_hour,
        followers=audience.followers,
        impressions=audience.impressions,
        reach=audience.reach
    )

    db.add(new_audience)
    db.commit()
    db.refresh(new_audience)

    return {
        "message": "Audience record created successfully",
        "data": audience_to_dict(new_audience)
    }


# =========================================================
# GET AUDIENCE RECORDS
# =========================================================

@router.get("/")
def get_audience_records(
    platform: Optional[str] = Query(
        default=None,
        description="Filter by platform. Use All or omit the parameter for all platforms."
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Audience).filter(
        Audience.creator_id == current_user.id
    )

    if platform and platform.strip().lower() != "all":
        query = query.filter(
            Audience.platform.ilike(
                platform.strip()
            )
        )

    records = query.order_by(
        Audience.id.asc()
    ).all()

    return {
        "message": "Audience records fetched successfully",
        "data": [
            audience_to_dict(record)
            for record in records
        ]
    }


# =========================================================
# GET AUDIENCE BY ID
# =========================================================

@router.get("/{audience_id}")
def get_audience_by_id(
    audience_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = (
        db.query(Audience)
        .filter(
            Audience.id == audience_id,
            Audience.creator_id == current_user.id
        )
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audience record not found"
        )

    return {
        "message": "Audience record fetched successfully",
        "data": audience_to_dict(record)
    }


# =========================================================
# UPDATE AUDIENCE
# =========================================================

@router.put("/{audience_id}")
def update_audience(
    audience_id: int,
    audience_data: AudienceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = (
        db.query(Audience)
        .filter(
            Audience.id == audience_id,
            Audience.creator_id == current_user.id
        )
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audience record not found"
        )

    update_data = audience_data.model_dump(
        exclude_unset=True
    )

    # Prevent ownership transfer
    if "creator_id" in update_data:

        if update_data["creator_id"] != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot transfer audience data to another creator"
            )

        update_data.pop("creator_id")

    for field, value in update_data.items():
        setattr(
            record,
            field,
            value
        )

    db.commit()
    db.refresh(record)

    return {
        "message": "Audience record updated successfully",
        "data": audience_to_dict(record)
    }


# =========================================================
# DELETE AUDIENCE
# =========================================================

@router.delete("/{audience_id}")
def delete_audience(
    audience_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = (
        db.query(Audience)
        .filter(
            Audience.id == audience_id,
            Audience.creator_id == current_user.id
        )
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audience record not found"
        )

    db.delete(record)
    db.commit()

    return {
        "message": "Audience record deleted successfully"
    }


# =========================================================
# AUDIENCE ANALYTICS ROUTER
# =========================================================

analytics_router = APIRouter(
    prefix="/analytics",
    tags=["Audience Analytics"]
)


# =========================================================
# AUDIENCE ANALYTICS
# =========================================================

@analytics_router.get("/audience")
def audience_analytics(
    platform: Optional[str] = Query(
        default=None,
        description="Filter audience analytics by platform. Use All or omit for all platforms."
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {
        "message": "Audience analytics fetched successfully",
        "data": get_audience_report(
            db,
            platform,
            current_user.id
        )
    }


# =========================================================
# GROWTH ANALYTICS
# =========================================================

@analytics_router.get("/growth")
def growth_analytics(
    platform: Optional[str] = Query(
        default=None,
        description="Filter growth analytics by platform. Use All or omit for all platforms."
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {
        "message": "Growth analytics fetched successfully",
        "data": get_growth_report(
            db,
            platform,
            current_user.id
        )
    }


# =========================================================
# AUDIENCE TRENDS
# =========================================================

@analytics_router.get("/audience-trends")
def audience_trends(
    platform: Optional[str] = Query(
        default=None,
        description="Filter audience trends by platform. Use All or omit for all platforms."
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {
        "message": "Audience trends fetched successfully",
        "data": get_audience_trends(
            db,
            platform,
            current_user.id
        )
    }