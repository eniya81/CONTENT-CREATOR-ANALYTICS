import os
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

from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse
)

from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ---------------------------------------------------------
# VERIFY USER ACCESS
# ---------------------------------------------------------

def verify_user_access(
    user_id: int,
    current_user: User
):
    """
    Ensure that a user can only access their own
    user-management record.
    """

    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own user data"
        )


# ---------------------------------------------------------
# CREATE USER
# ---------------------------------------------------------

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a user.

    Authentication is required.
    """

    return UserService.create(
        db,
        user
    )


# ---------------------------------------------------------
# GET ALL USERS
# ---------------------------------------------------------

@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Return users visible to the authenticated user.

    Only the authenticated user's own record is returned.
    """

    return UserService.get_all(
        db,
        current_user.id
    )


# ---------------------------------------------------------
# SEARCH USERS BY ROLE
# ---------------------------------------------------------

@router.get(
    "/search",
    response_model=list[UserResponse]
)
def search_users(
    role: Optional[str] = Query(
        default=None,
        description="Filter users by role"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Search users.

    Example:

        GET /users/search?role=creator

    Results are scoped to the authenticated user.
    """

    return UserService.search(
        db,
        current_user.id,
        role
    )


# ---------------------------------------------------------
# GET USER BY ID
# ---------------------------------------------------------

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific user.

    A user cannot retrieve another user's record.
    """

    verify_user_access(
        user_id,
        current_user
    )

    return UserService.get_by_id(
        db,
        user_id
    )


# ---------------------------------------------------------
# UPDATE USER
# ---------------------------------------------------------

@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update the authenticated user's own profile.

    Role changes are intentionally not permitted.
    """

    verify_user_access(
        user_id,
        current_user
    )

    return UserService.update(
        db,
        user_id,
        user
    )


# ---------------------------------------------------------
# DELETE USER
# ---------------------------------------------------------

@router.delete(
    "/{user_id}"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete the authenticated user's own account.
    """

    verify_user_access(
        user_id,
        current_user
    )

    return UserService.delete(
        db,
        user_id
    )