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
from app.models.content import Content
from app.schemas.content import ContentCreate, ContentUpdate


router = APIRouter(
    prefix="/content",
    tags=["Content"]
)


# ---------------------------------------------------------
# CREATOR ACCESS HELPER
# ---------------------------------------------------------

def verify_creator_access(
    creator_id: int,
    current_user: User
):
    if current_user.id != creator_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own content"
        )


# ---------------------------------------------------------
# CONTENT RESPONSE HELPER
# ---------------------------------------------------------

def content_response(content: Content):
    return {
        "id": content.id,
        "creator_id": content.creator_id,
        "platform": content.platform,
        "content_title": content.content_title,
        "views": content.views,
        "likes": content.likes,
        "comments": content.comments,
        "shares": content.shares,
        "saves": content.saves,
        "watch_time": content.watch_time,
        "reach": content.reach,
        "published_date": content.published_date
    }


# ---------------------------------------------------------
# CREATE CONTENT
# ---------------------------------------------------------

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def create_content(
    content: ContentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # A creator can only create content for their own account
    verify_creator_access(
        content.creator_id,
        current_user
    )

    new_content = Content(
        creator_id=content.creator_id,
        platform=content.platform,
        content_title=content.content_title,
        views=content.views,
        likes=content.likes,
        comments=content.comments,
        shares=content.shares,
        saves=content.saves,
        watch_time=content.watch_time,
        reach=content.reach,
        published_date=content.published_date
    )

    db.add(new_content)
    db.commit()
    db.refresh(new_content)

    return {
        "message": "Content created successfully",
        "data": content_response(new_content)
    }


# ---------------------------------------------------------
# GET ALL CONTENT / FILTER BY PLATFORM
# ---------------------------------------------------------

@router.get("/")
def get_contents(
    platform: Optional[str] = Query(
        default=None,
        description="Filter content by platform. Use All or omit for all platforms."
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only return content belonging to the authenticated creator
    query = db.query(Content).filter(
        Content.creator_id == current_user.id
    )

    if platform and platform.strip().lower() != "all":
        query = query.filter(
            Content.platform.ilike(
                platform.strip()
            )
        )

    contents = query.order_by(
        Content.published_date.desc(),
        Content.id.desc()
    ).all()

    result = [
        content_response(content)
        for content in contents
    ]

    return {
        "message": "Content fetched successfully",
        "data": result
    }


# ---------------------------------------------------------
# GET SINGLE CONTENT
# ---------------------------------------------------------

@router.get("/{content_id}")
def get_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    content = (
        db.query(Content)
        .filter(
            Content.id == content_id,
            Content.creator_id == current_user.id
        )
        .first()
    )

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    return {
        "message": "Content fetched successfully",
        "data": content_response(content)
    }


# ---------------------------------------------------------
# UPDATE CONTENT
# ---------------------------------------------------------

@router.put("/{content_id}")
def update_content(
    content_id: int,
    content_data: ContentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    content = (
        db.query(Content)
        .filter(
            Content.id == content_id,
            Content.creator_id == current_user.id
        )
        .first()
    )

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    update_data = content_data.model_dump(
        exclude_unset=True
    )

    # Prevent changing ownership of existing content
    if "creator_id" in update_data:
        if update_data["creator_id"] != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot transfer content to another creator"
            )

        update_data.pop("creator_id")

    for field, value in update_data.items():
        setattr(
            content,
            field,
            value
        )

    db.commit()
    db.refresh(content)

    return {
        "message": "Content updated successfully",
        "data": content_response(content)
    }


# ---------------------------------------------------------
# DELETE CONTENT
# ---------------------------------------------------------

@router.delete("/{content_id}")
def delete_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    content = (
        db.query(Content)
        .filter(
            Content.id == content_id,
            Content.creator_id == current_user.id
        )
        .first()
    )

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    db.delete(content)
    db.commit()

    return {
        "message": "Content deleted successfully"
    }