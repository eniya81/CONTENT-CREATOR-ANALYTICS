from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import OAuth2PasswordBearer

from jose import (
    JWTError,
    jwt
)

from sqlalchemy.orm import Session

from app.core.security import (
    SECRET_KEY,
    ALGORITHM
)

from app.db.database import get_db

from app.models.user import User

from app.schemas.user import TokenData


# =========================================================
# OAUTH2 CONFIGURATION
# =========================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# =========================================================
# GET CURRENT USER
# =========================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Validate the JWT access token and return the
    currently authenticated user.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if not email or not isinstance(email, str):
            raise credentials_exception

        token_data = TokenData(
            email=email
        )

    except JWTError:
        raise credentials_exception

    except ValueError:
        raise credentials_exception

    user = (
        db.query(User)
        .filter(
            User.email == token_data.email
        )
        .first()
    )

    if user is None:
        raise credentials_exception

    return user