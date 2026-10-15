from sqlalchemy import Column, Index, Integer, String

from app.db.database import Base


class Audience(Base):
    __tablename__ = "audience"

    id = Column(Integer, primary_key=True, index=True)

    creator_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    # Platform is nullable temporarily so existing audience
    # records in PostgreSQL are not broken.
    platform = Column(
        String(50),
        nullable=True,
        index=True
    )

    age_group = Column(
        String(50),
        nullable=False
    )

    gender = Column(
        String(20),
        nullable=False
    )

    country = Column(
        String(100),
        nullable=False
    )

    city = Column(
        String(100),
        nullable=False
    )

    device_type = Column(
        String(50),
        nullable=False
    )

    active_hour = Column(
        Integer,
        nullable=False
    )

    followers = Column(
        Integer,
        nullable=False,
        default=0
    )

    impressions = Column(
        Integer,
        nullable=False,
        default=0
    )

    reach = Column(
        Integer,
        nullable=False,
        default=0
    )

    __table_args__ = (
        Index(
            "ix_audience_creator_platform",
            "creator_id",
            "platform"
        ),
    )