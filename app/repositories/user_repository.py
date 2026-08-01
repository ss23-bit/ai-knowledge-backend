from sqlalchemy import select, func
from sqlalchemy.orm import Session
from _collections_abc import Sequence

from app.models.user import User

SORT_FIELD = {
    "id": User.id,
    "email": User.email,
    "full_name": User.full_name,
}

def create_user(
        db: Session,
        email: str,
        full_name: str,
) -> User:

    user = User(
        email=email,
        full_name=full_name,
    )

    db.add(user)

    try:
        db.commit()
    except:
        # If it's in failed transaction state, the session will refuse to execute more SQL.
        # Rollback repairs the Session so it can start a new transaction
        db.rollback()
        raise

    db.refresh(user)

    return user

def get_user_by_id(
        db: Session,
        user_id: int,
) -> User | None:

    stmt = (
        select(User)
        .where(User.id == user_id)
    )

    return db.scalar(stmt)

def get_all_users(
        db: Session,
        limit: int,
        offset: int,
        search: str | None,
        sort: str | None,
) -> tuple[Sequence[User], int]:
    # DRY, building conditions for reusable quries.
    filters = []

    if search:
        filters.append(
                # ilike is Case-insensitive LIKE
                User.full_name.ilike(f"%{search}%")
        )

    stmt = (
        select(User)
    )

    count_stmt = (
        select(func.count()).select_from(User)
    )


    if filters:
        stmt = (
            stmt
            .where(*filters)
        )

    if filters:
        count_stmt = (
            count_stmt.where(*filters)
        )

    if sort:
        descending = sort.startswith("-")
        sort_field = sort.removeprefix("-")

        column = SORT_FIELD.get(sort_field)
        if column is None:
            raise ValueError(f"Invalid sort field: {sort_field}")

        if descending:
            stmt = (
                stmt
                .order_by(column.desc())
            )
        else:
            stmt = (
                stmt
                .order_by(column)
            )             

    stmt = (
        stmt
        .limit(limit)
        .offset(offset)
    )

    # collec them into python list, but SQLAlchemy telling it'll be Sequence.
    users = db.scalars(stmt).all()

    total = db.scalar(count_stmt) or 0

    # Python will return the values as tuple
    return users, total

def update_user(
        db: Session,
        user: User,
        full_name: str,
) -> User:
    # Makes Dirty state
    user.full_name = full_name

    db.commit()

    db.refresh(user)

    return user

def delete_user(
        db: Session,
        user: User,
) -> None:

    db.delete(user)

    db.commit()