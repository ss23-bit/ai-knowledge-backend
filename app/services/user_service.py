from sqlalchemy.orm import Session

from app.repositories.user_repository import create_user, get_user_by_id
from app.models.user import User

def register_user(
        db: Session,
        email: str,
        full_name: str,
) -> User:

    return create_user(
        # "=" makes Python matches by name, not by position.
        db=db,
        email=email,
        full_name=full_name,
    )

def find_user_by_id(
        db: Session,
        user_id: int,
) -> User | None:

    return get_user_by_id(
        db=db,
        user_id=user_id,
    )