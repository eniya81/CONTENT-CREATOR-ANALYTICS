from datetime import date
import sys

from app.db.database import SessionLocal
from app.models.content import Content


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

DEFAULT_CREATOR_ID = 1


# ---------------------------------------------------------
# Meaningful multi-platform sample data
# ---------------------------------------------------------
#
# These are database seed records only.
# Analytics are still calculated by the backend services.
#
# Each platform has multiple records with:
# - different content IDs
# - different dates
# - different performance metrics
# ---------------------------------------------------------

MULTI_PLATFORM_CONTENT = [
    # =====================================================
    # YouTube
    # =====================================================

    {
        "platform": "YouTube",
        "external_content_id": "YT-MP-001",
        "content_title": "Python Tutorial",
        "views": 15000,
        "likes": 1200,
        "comments": 150,
        "shares": 100,
        "saves": 80,
        "watch_time": 5200,
        "reach": 18000,
        "published_date": date(2026, 8, 10),
    },
    {
        "platform": "YouTube",
        "external_content_id": "YT-MP-002",
        "content_title": "FastAPI Beginner Guide",
        "views": 12000,
        "likes": 950,
        "comments": 120,
        "shares": 85,
        "saves": 60,
        "watch_time": 4300,
        "reach": 15000,
        "published_date": date(2026, 8, 17),
    },
    {
        "platform": "YouTube",
        "external_content_id": "YT-MP-003",
        "content_title": "PostgreSQL for Developers",
        "views": 22000,
        "likes": 1800,
        "comments": 230,
        "shares": 160,
        "saves": 110,
        "watch_time": 6800,
        "reach": 26000,
        "published_date": date(2026, 8, 24),
    },
    {
        "platform": "YouTube",
        "external_content_id": "YT-MP-004",
        "content_title": "REST API Design Best Practices",
        "views": 18500,
        "likes": 1450,
        "comments": 175,
        "shares": 130,
        "saves": 95,
        "watch_time": 5900,
        "reach": 22000,
        "published_date": date(2026, 8, 31),
    },

    # =====================================================
    # Instagram
    # =====================================================

    {
        "platform": "Instagram",
        "external_content_id": "IG-MP-001",
        "content_title": "Python Reels",
        "views": 18000,
        "likes": 2100,
        "comments": 260,
        "shares": 180,
        "saves": 300,
        "watch_time": 3900,
        "reach": 22000,
        "published_date": date(2026, 8, 9),
    },
    {
        "platform": "Instagram",
        "external_content_id": "IG-MP-002",
        "content_title": "Coding Tips",
        "views": 14000,
        "likes": 1700,
        "comments": 190,
        "shares": 140,
        "saves": 220,
        "watch_time": 3200,
        "reach": 18000,
        "published_date": date(2026, 8, 16),
    },
    {
        "platform": "Instagram",
        "external_content_id": "IG-MP-003",
        "content_title": "Developer Productivity Tips",
        "views": 24500,
        "likes": 2900,
        "comments": 340,
        "shares": 260,
        "saves": 480,
        "watch_time": 5100,
        "reach": 29000,
        "published_date": date(2026, 8, 23),
    },
    {
        "platform": "Instagram",
        "external_content_id": "IG-MP-004",
        "content_title": "API Development Carousel",
        "views": 20500,
        "likes": 2350,
        "comments": 280,
        "shares": 210,
        "saves": 390,
        "watch_time": 4400,
        "reach": 25000,
        "published_date": date(2026, 8, 30),
    },

    # =====================================================
    # TikTok
    # =====================================================

    {
        "platform": "TikTok",
        "external_content_id": "TT-MP-001",
        "content_title": "Learn Python in 60 Seconds",
        "views": 25000,
        "likes": 3200,
        "comments": 340,
        "shares": 420,
        "saves": 500,
        "watch_time": 4100,
        "reach": 30000,
        "published_date": date(2026, 8, 8),
    },
    {
        "platform": "TikTok",
        "external_content_id": "TT-MP-002",
        "content_title": "Python Coding Trick",
        "views": 32000,
        "likes": 4500,
        "comments": 510,
        "shares": 620,
        "saves": 780,
        "watch_time": 5200,
        "reach": 38000,
        "published_date": date(2026, 8, 15),
    },
    {
        "platform": "TikTok",
        "external_content_id": "TT-MP-003",
        "content_title": "FastAPI in One Minute",
        "views": 28500,
        "likes": 3900,
        "comments": 430,
        "shares": 540,
        "saves": 690,
        "watch_time": 4700,
        "reach": 34000,
        "published_date": date(2026, 8, 22),
    },
    {
        "platform": "TikTok",
        "external_content_id": "TT-MP-004",
        "content_title": "3 Backend Mistakes to Avoid",
        "views": 41000,
        "likes": 5800,
        "comments": 720,
        "shares": 850,
        "saves": 920,
        "watch_time": 6100,
        "reach": 48000,
        "published_date": date(2026, 8, 29),
    },

    # =====================================================
    # Facebook
    # =====================================================

    {
        "platform": "Facebook",
        "external_content_id": "FB-MP-001",
        "content_title": "Python Career Tips",
        "views": 10000,
        "likes": 800,
        "comments": 110,
        "shares": 90,
        "saves": 50,
        "watch_time": 3000,
        "reach": 13500,
        "published_date": date(2026, 8, 7),
    },
    {
        "platform": "Facebook",
        "external_content_id": "FB-MP-002",
        "content_title": "Backend Developer Roadmap",
        "views": 13500,
        "likes": 1100,
        "comments": 145,
        "shares": 160,
        "saves": 80,
        "watch_time": 3600,
        "reach": 17000,
        "published_date": date(2026, 8, 14),
    },
    {
        "platform": "Facebook",
        "external_content_id": "FB-MP-003",
        "content_title": "Learn APIs from Scratch",
        "views": 16800,
        "likes": 1420,
        "comments": 190,
        "shares": 210,
        "saves": 105,
        "watch_time": 4200,
        "reach": 20500,
        "published_date": date(2026, 8, 21),
    },
    {
        "platform": "Facebook",
        "external_content_id": "FB-MP-004",
        "content_title": "Developer Interview Preparation",
        "views": 19200,
        "likes": 1650,
        "comments": 220,
        "shares": 250,
        "saves": 130,
        "watch_time": 4700,
        "reach": 23000,
        "published_date": date(2026, 8, 28),
    },

    # =====================================================
    # LinkedIn
    # =====================================================

    {
        "platform": "LinkedIn",
        "external_content_id": "LI-MP-001",
        "content_title": "Building APIs with FastAPI",
        "views": 8500,
        "likes": 620,
        "comments": 95,
        "shares": 70,
        "saves": 45,
        "watch_time": 2800,
        "reach": 11000,
        "published_date": date(2026, 8, 6),
    },
    {
        "platform": "LinkedIn",
        "external_content_id": "LI-MP-002",
        "content_title": "PostgreSQL Development Guide",
        "views": 10500,
        "likes": 810,
        "comments": 120,
        "shares": 105,
        "saves": 65,
        "watch_time": 3200,
        "reach": 13500,
        "published_date": date(2026, 8, 13),
    },
    {
        "platform": "LinkedIn",
        "external_content_id": "LI-MP-003",
        "content_title": "How I Built a Creator Analytics System",
        "views": 14500,
        "likes": 1250,
        "comments": 185,
        "shares": 160,
        "saves": 95,
        "watch_time": 4100,
        "reach": 18000,
        "published_date": date(2026, 8, 20),
    },
    {
        "platform": "LinkedIn",
        "external_content_id": "LI-MP-004",
        "content_title": "Backend Engineering Best Practices",
        "views": 12800,
        "likes": 1080,
        "comments": 150,
        "shares": 135,
        "saves": 80,
        "watch_time": 3700,
        "reach": 16000,
        "published_date": date(2026, 8, 27),
    },

    # =====================================================
    # X
    # =====================================================

    {
        "platform": "X",
        "external_content_id": "X-MP-001",
        "content_title": "Python Development Tips",
        "views": 7000,
        "likes": 500,
        "comments": 80,
        "shares": 60,
        "saves": 30,
        "watch_time": 1800,
        "reach": 9000,
        "published_date": date(2026, 8, 5),
    },
    {
        "platform": "X",
        "external_content_id": "X-MP-002",
        "content_title": "Useful Python Libraries",
        "views": 9200,
        "likes": 760,
        "comments": 105,
        "shares": 130,
        "saves": 55,
        "watch_time": 2200,
        "reach": 11500,
        "published_date": date(2026, 8, 12),
    },
    {
        "platform": "X",
        "external_content_id": "X-MP-003",
        "content_title": "FastAPI Development Thread",
        "views": 11800,
        "likes": 980,
        "comments": 135,
        "shares": 180,
        "saves": 75,
        "watch_time": 2700,
        "reach": 14500,
        "published_date": date(2026, 8, 19),
    },
    {
        "platform": "X",
        "external_content_id": "X-MP-004",
        "content_title": "Backend Engineering Lessons",
        "views": 13500,
        "likes": 1150,
        "comments": 160,
        "shares": 220,
        "saves": 90,
        "watch_time": 3100,
        "reach": 16500,
        "published_date": date(2026, 8, 26),
    },
]


# ---------------------------------------------------------
# Seed function
# ---------------------------------------------------------

def seed_multiplatform_data(creator_id: int):
    db = SessionLocal()

    inserted = 0
    skipped = 0

    try:
        for record in MULTI_PLATFORM_CONTENT:

            # -------------------------------------------------
            # Idempotency check
            # -------------------------------------------------
            #
            # If this external content ID already exists for
            # this creator, don't insert it again.
            # -------------------------------------------------

            existing = (
                db.query(Content)
                .filter(
                    Content.creator_id == creator_id,
                    Content.external_content_id
                    == record["external_content_id"],
                )
                .first()
            )

            if existing:
                skipped += 1
                continue

            content = Content(
                creator_id=creator_id,
                platform=record["platform"],
                external_content_id=record["external_content_id"],
                content_title=record["content_title"],
                views=record["views"],
                likes=record["likes"],
                comments=record["comments"],
                shares=record["shares"],
                saves=record["saves"],
                watch_time=record["watch_time"],
                reach=record["reach"],
                published_date=record["published_date"],
            )

            db.add(content)
            inserted += 1

        db.commit()

        print("=" * 60)
        print("MULTI-PLATFORM DATA SEED COMPLETED")
        print("=" * 60)
        print(f"Creator ID : {creator_id}")
        print(f"Inserted   : {inserted}")
        print(f"Skipped    : {skipped}")
        print(f"Total seed records : {len(MULTI_PLATFORM_CONTENT)}")
        print("=" * 60)

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    creator_id = DEFAULT_CREATOR_ID

    if len(sys.argv) > 1:
        try:
            creator_id = int(sys.argv[1])
        except ValueError:
            print("Creator ID must be an integer.")
            sys.exit(1)

    seed_multiplatform_data(creator_id)