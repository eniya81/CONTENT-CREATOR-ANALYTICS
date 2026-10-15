from sqlalchemy.orm import Session

from app.services.analytics_service import (
    get_summary,
    get_top_content,
    get_platform_comparison
)

from app.services.audience_service import (
    get_audience_report,
    get_growth_report
)

from app.services.revenue_service import (
    get_total_revenue,
    get_revenue_by_source,
    get_monthly_revenue
)


def generate_creator_report(
    db: Session,
    creator_id: int
):
    """
    Generate a complete analytics report for one creator.

    All analytics, audience, growth, and revenue data
    is scoped to the supplied creator_id.
    """

    # -----------------------------------------------------
    # CONTENT PERFORMANCE
    # -----------------------------------------------------

    analytics_summary = get_summary(
        db,
        creator_id=creator_id
    )

    top_content = get_top_content(
        db,
        creator_id=creator_id
    )

    # -----------------------------------------------------
    # PLATFORM COMPARISON
    # -----------------------------------------------------

    platform_comparison = get_platform_comparison(
        db,
        creator_id=creator_id
    )

    # -----------------------------------------------------
    # AUDIENCE ANALYTICS
    # -----------------------------------------------------

    audience_report = get_audience_report(
        db,
        creator_id=creator_id
    )

    # -----------------------------------------------------
    # GROWTH & TRENDS
    # -----------------------------------------------------

    growth_report = get_growth_report(
        db,
        creator_id=creator_id
    )

    # -----------------------------------------------------
    # REVENUE ANALYTICS
    # -----------------------------------------------------

    total_revenue = get_total_revenue(
        db,
        creator_id
    )

    revenue_by_source = get_revenue_by_source(
        db,
        creator_id
    )

    monthly_revenue = get_monthly_revenue(
        db,
        creator_id
    )

    # -----------------------------------------------------
    # FINAL REPORT
    # -----------------------------------------------------

    return {
        "creator_id": creator_id,

        "content_performance": {
            "summary": analytics_summary,
            "top_content": top_content
        },

        "audience_analytics": audience_report,

        "revenue_analytics": {
            "total_revenue": total_revenue,
            "revenue_by_source": revenue_by_source,
            "monthly_revenue": monthly_revenue
        },

        "growth_trends": growth_report,

        "platform_comparison": platform_comparison
    }