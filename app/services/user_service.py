from sqlalchemy.orm import Session
from _collections_abc import Sequence

from app.repositories.user_repository import create_user, get_user_by_id, get_all_users, update_user, delete_user
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

def list_users(
        db: Session,
        limit: int,
        offset: int,
        search: str | None,
        sort: str | None,
) -> tuple[Sequence[User], int]:

    return get_all_users(
        db=db,
        limit=limit,
        offset=offset,
        search=search,
        sort=sort,
    )

def update_user_name(
        db: Session,
        user_id: int,
        full_name: str,
) -> User | None:

    user = get_user_by_id(
        db=db,
        user_id=user_id,
    )

    if user is None:
        return None

    return update_user(
        db=db,
        user=user,
        full_name=full_name,
    )

def delete_user_by_id(
        db: Session,
        user_id: int,
) -> bool:

    user = get_user_by_id(
        db=db,
        user_id=user_id
    )

    if user is None:
        return False

    delete_user(
        db=db,
        user=user
    )

    return True