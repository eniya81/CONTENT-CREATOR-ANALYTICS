import os
from dotenv import load_dotenv

load_dotenv()
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt
from passlib.context import CryptContext


# =========================================================
# PASSWORD HASHING
# =========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    """
    Hash a plain-text password.
    """

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify a plain-text password against its stored hash.
    """

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# =========================================================
# JWT CONFIGURATION
# =========================================================

# Read the secret from an environment variable.
#
# IMPORTANT:
# Set JWT_SECRET_KEY in your environment before running
# the application.
#
# The fallback below is only intended to prevent the
# application from crashing during local development.
# It should NOT be used in production.

SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "development-only-change-this-secret"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# =========================================================
# CREATE ACCESS TOKEN
# =========================================================

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a signed JWT access token.
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )