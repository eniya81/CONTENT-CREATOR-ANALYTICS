from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


class UserService:

    # ---------------------------------------------------------
    # CREATE USER
    # ---------------------------------------------------------

    @staticmethod
    def create(
        db: Session,
        user_in: UserCreate
    ):
        """
        Create a new user with a securely hashed password.
        """

        existing_user = (
            db.query(User)
            .filter(User.email == user_in.email)
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        db_user = User(
            full_name=user_in.full_name,
            email=user_in.email,
            hashed_password=hash_password(
                user_in.password
            ),
            role=user_in.role
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    # ---------------------------------------------------------
    # GET ALL USERS
    # ---------------------------------------------------------

    @staticmethod
    def get_all(
        db: Session,
        creator_id: Optional[int] = None
    ):
        """
        Return users.

        If creator_id is supplied, only that user's
        record is returned.
        """

        query = db.query(User)

        if creator_id is not None:
            query = query.filter(
                User.id == creator_id
            )

        return (
            query
            .order_by(User.id.asc())
            .all()
        )

    # ---------------------------------------------------------
    # GET USER BY ID
    # ---------------------------------------------------------

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: int
    ):
        """
        Retrieve a user by ID.
        """

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user

    # ---------------------------------------------------------
    # SEARCH USERS
    # ---------------------------------------------------------

    @staticmethod
    def search(
        db: Session,
        creator_id: Optional[int] = None,
        role: Optional[str] = None
    ):
        """
        Search users.

        Results can be restricted to the authenticated
        creator and optionally filtered by role.
        """

        query = db.query(User)

        if creator_id is not None:
            query = query.filter(
                User.id == creator_id
            )

        if role:
            query = query.filter(
                User.role.ilike(role.strip())
            )

        return (
            query
            .order_by(User.id.asc())
            .all()
        )

    # ---------------------------------------------------------
    # UPDATE USER
    # ---------------------------------------------------------

    @staticmethod
    def update(
        db: Session,
        user_id: int,
        user_in: UserUpdate
    ):
        """
        Update a user's profile.

        Role changes are not permitted.
        """

        user = UserService.get_by_id(
            db,
            user_id
        )

        # Update full name
        if user_in.full_name is not None:
            user.full_name = user_in.full_name

        # Update email
        if user_in.email is not None:

            existing_user = (
                db.query(User)
                .filter(
                    User.email == user_in.email,
                    User.id != user_id
                )
                .first()
            )

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )

            user.email = user_in.email

        # Update password through normal profile update
        if user_in.password is not None:
            user.hashed_password = hash_password(
                user_in.password
            )

        # Prevent role modification
        if user_in.role is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Changing user role is not permitted"
            )

        db.commit()
        db.refresh(user)

        return user

    # ---------------------------------------------------------
    # DELETE USER
    # ---------------------------------------------------------

    @staticmethod
    def delete(
        db: Session,
        user_id: int
    ):
        """
        Delete a user.
        """

        user = UserService.get_by_id(
            db,
            user_id
        )

        db.delete(user)
        db.commit()

        return {
            "message": "User deleted successfully"
        }

   