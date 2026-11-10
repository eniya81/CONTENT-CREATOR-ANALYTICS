"""Create missing application tables and indexes.

Revision ID: 18bb2b761651
Revises: 4adf27b62789
"""

from typing import Sequence, Union

from alembic import op

from app.db.database import Base

# Import all models so their tables are registered with Base.metadata.
from app.models.user import User
from app.models.content import Content
from app.models.revenue import Revenue
from app.models.sponsorship import Sponsorship
from app.models.notification import Notification

import app.models.audience
import app.models.growth


revision: str = "18bb2b761651"
down_revision: Union[str, Sequence[str], None] = "4adf27b62789"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create any missing application tables and their indexes."""

    # Existing tables are preserved.
    # Missing tables and their indexes are created.
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    """No automatic deletion of application tables."""

    pass