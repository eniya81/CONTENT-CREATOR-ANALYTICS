from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.auth import get_current_user
from app.models.user import User

from app.schemas.notification import (
    NotificationCreate,
    NotificationResponse,
    NotificationUpdate,
)

from app.services.notification_service import (
    create_notification,
    get_notifications,
    get_notification,
    update_notification,
    delete_notification,
    generate_performance_alert,
    generate_engagement_notification,
    generate_revenue_alert,
)


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


# =========================================================
# AUTHORIZATION HELPER
# =========================================================

def verify_creator_access(
    creator_id: int,
    current_user: User,
):
    """
    Ensure the requested creator belongs to the
    currently authenticated user.
    """

    if current_user.id != creator_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own notifications",
        )


# =========================================================
# ALERT APIs
# =========================================================
# Keep these BEFORE /{notification_id}
# so "alerts" is not interpreted as an integer ID.
# =========================================================


@router.post(
    "/alerts/performance/{creator_id}",
    response_model=NotificationResponse,
)
def performance_alert(
    creator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_creator_access(
        creator_id,
        current_user,
    )

    notification = generate_performance_alert(
        db,
        creator_id,
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No content available for performance analysis",
        )

    return notification


@router.post(
    "/alerts/engagement/{creator_id}",
    response_model=NotificationResponse,
)
def engagement_alert(
    creator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_creator_access(
        creator_id,
        current_user,
    )

    notification = generate_engagement_notification(
        db,
        creator_id,
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unable to generate engagement notification",
        )

    return notification


@router.post(
    "/alerts/revenue/{creator_id}",
    response_model=NotificationResponse,
)
def revenue_alert(
    creator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_creator_access(
        creator_id,
        current_user,
    )

    notification = generate_revenue_alert(
        db,
        creator_id,
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unable to generate revenue notification",
        )

    return notification


# =========================================================
# NOTIFICATION CRUD
# =========================================================


@router.post(
    "/",
    response_model=NotificationResponse,
)
def create_notification_api(
    notification_data: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_creator_access(
        notification_data.creator_id,
        current_user,
    )

    return create_notification(
        db,
        notification_data,
    )


@router.get(
    "/",
    response_model=list[NotificationResponse],
)
def get_notifications_api(
    creator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_creator_access(
        creator_id,
        current_user,
    )

    return get_notifications(
        db,
        creator_id,
    )


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
)
def get_notification_api(
    notification_id: int,
    creator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_creator_access(
        creator_id,
        current_user,
    )

    notification = get_notification(
        db,
        notification_id,
        creator_id,
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    return notification


@router.put(
    "/{notification_id}",
    response_model=NotificationResponse,
)
def update_notification_api(
    notification_id: int,
    creator_id: int,
    notification_data: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_creator_access(
        creator_id,
        current_user,
    )

    notification = update_notification(
        db,
        notification_id,
        creator_id,
        notification_data,
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    return notification


@router.delete(
    "/{notification_id}",
)
def delete_notification_api(
    notification_id: int,
    creator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_creator_access(
        creator_id,
        current_user,
    )

    notification = delete_notification(
        db,
        notification_id,
        creator_id,
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    return {
        "message": "Notification deleted successfully",
    }