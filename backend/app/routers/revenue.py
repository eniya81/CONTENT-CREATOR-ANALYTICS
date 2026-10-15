from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.auth import get_current_user
from app.models.user import User

from app.schemas.revenue import (
    RevenueCreate,
    RevenueUpdate,
)

from app.services.revenue_service import (
    create_revenue,
    get_revenues,
    get_revenue_by_id,
    update_revenue,
    delete_revenue,
    get_total_revenue,
    get_revenue_by_source,
    get_monthly_revenue,
    get_revenue_trend,
)


router = APIRouter(
    prefix="/revenue",
    tags=["Revenue"],
)


# ==================================================
# AUTHORIZATION HELPER
# ==================================================

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
            detail="You can only access your own revenue data",
        )


# ==================================================
# REVENUE ANALYTICS
# IMPORTANT:
# These routes are placed BEFORE /{revenue_id}
# ==================================================


# --------------------------------------------------
# TOTAL REVENUE
# GET /revenue/analytics/summary?creator_id=1
# --------------------------------------------------

@router.get("/analytics/summary")
def revenue_summary(
    creator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_creator_access(
        creator_id,
        current_user,
    )

    total = get_total_revenue(
        db,
        creator_id,
    )

    return {
        "creator_id": creator_id,
        "total_revenue": total,
    }


# --------------------------------------------------
# REVENUE BY SOURCE
# GET /revenue/analytics/by-source?creator_id=1
# --------------------------------------------------

@router.get("/analytics/by-source")
def revenue_by_source(
    creator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_creator_access(
        creator_id,
        current_user,
    )

    result = get_revenue_by_source(
        db,
        creator_id,
    )

    return {
        "creator_id": creator_id,
        "revenue_by_source": result,
    }


# --------------------------------------------------
# MONTHLY REVENUE
# GET /revenue/analytics/monthly?creator_id=1
# --------------------------------------------------

@router.get("/analytics/monthly")
def monthly_revenue(
    creator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_creator_access(
        creator_id,
        current_user,
    )

    result = get_monthly_revenue(
        db,
        creator_id,
    )

    return {
        "creator_id": creator_id,
        "data": result,
    }


# --------------------------------------------------
# REVENUE TREND
# GET /revenue/analytics/trend?creator_id=1
# --------------------------------------------------

@router.get("/analytics/trend")
def revenue_trend(
    creator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_creator_access(
        creator_id,
        current_user,
    )

    result = get_revenue_trend(
        db,
        creator_id,
    )

    return {
        "creator_id": creator_id,
        "data": result,
    }


# ==================================================
# CREATE REVENUE
# POST /revenue/
# ==================================================

@router.post("/")
def create_revenue_record(
    revenue_data: RevenueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # RevenueCreate is expected to contain creator_id.
    verify_creator_access(
        revenue_data.creator_id,
        current_user,
    )

    revenue = create_revenue(
        db,
        revenue_data,
    )

    return {
        "message": "Revenue created successfully",
        "data": revenue,
    }


# ==================================================
# GET ALL REVENUE FOR CREATOR
# GET /revenue/?creator_id=1
# ==================================================

@router.get("/")
def get_all_revenue(
    creator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_creator_access(
        creator_id,
        current_user,
    )

    revenues = get_revenues(
        db,
        creator_id,
    )

    return {
        "message": "Revenue records fetched successfully",
        "data": revenues,
    }


# ==================================================
# GET REVENUE BY ID
# GET /revenue/{revenue_id}?creator_id=1
# ==================================================

@router.get("/{revenue_id}")
def get_single_revenue(
    revenue_id: int,
    creator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_creator_access(
        creator_id,
        current_user,
    )

    revenue = get_revenue_by_id(
        db,
        revenue_id,
        creator_id,
    )

    if not revenue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Revenue record not found",
        )

    return {
        "message": "Revenue record fetched successfully",
        "data": revenue,
    }


# ==================================================
# UPDATE REVENUE
# PUT /revenue/{revenue_id}?creator_id=1
# ==================================================

@router.put("/{revenue_id}")
def update_revenue_record(
    revenue_id: int,
    creator_id: int,
    revenue_data: RevenueUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_creator_access(
        creator_id,
        current_user,
    )

    revenue = get_revenue_by_id(
        db,
        revenue_id,
        creator_id,
    )

    if not revenue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Revenue record not found",
        )

    updated_revenue = update_revenue(
        db,
        revenue,
        revenue_data,
    )

    return {
        "message": "Revenue updated successfully",
        "data": updated_revenue,
    }


# ==================================================
# DELETE REVENUE
# DELETE /revenue/{revenue_id}?creator_id=1
# ==================================================

@router.delete("/{revenue_id}")
def delete_revenue_record(
    revenue_id: int,
    creator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_creator_access(
        creator_id,
        current_user,
    )

    revenue = get_revenue_by_id(
        db,
        revenue_id,
        creator_id,
    )

    if not revenue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Revenue record not found",
        )

    delete_revenue(
        db,
        revenue,
    )

    return {
        "message": "Revenue deleted successfully",
    }