from sqlalchemy import Column, Date, Float, Index, Integer, String

from app.db.database import Base


class Growth(Base):
    __tablename__ = "growth"

    id = Column(Integer, primary_key=True, index=True)

    creator_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    platform = Column(
        String(50),
        nullable=True,
        index=True
    )

    date = Column(
        Date,
        nullable=False
    )

    followers = Column(
        Integer,
        nullable=False,
        default=0
    )

    reach = Column(
        Integer,
        nullable=False,
        default=0
    )

    engagement_rate = Column(
        Float,
        nullable=False,
        default=0.0
    )

    __table_args__ = (
        Index(
            "ix_growth_creator_platform",
            "creator_id",
            "platform"
        ),
    )