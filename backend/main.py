from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.users import router as user_router
from app.routers.auth import router as auth_router
from app.routers.content import router as content_router
from app.routers.analytics import router as analytics_router

from app.routers.audience import (
    router as audience_router,
    analytics_router as audience_analytics_router
)

from app.routers.social import router as social_router
from app.routers.revenue import router as revenue_router
from app.routers.sponsorship import router as sponsorship_router
from app.routers.notifications import router as notifications_router
from app.routers.reports import router as reports_router

app = FastAPI(
    title="Creator Analytics Content Performance Dashboard"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://creator-analytics-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(content_router)
app.include_router(analytics_router)
app.include_router(audience_router)
app.include_router(audience_analytics_router)
app.include_router(social_router)
app.include_router(revenue_router)
app.include_router(sponsorship_router)
app.include_router(notifications_router)
app.include_router(reports_router)


@app.get("/")
def root():
    return {"message": "API is running!"}