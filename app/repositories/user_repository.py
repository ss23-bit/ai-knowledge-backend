from sqlalchemy import select
from sqlalchemy.orm import Session
from _collections_abc import Sequence

from app.models.user import User

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
) -> Sequence[User]:
    
    stmt = select(User)

    # collec them into python list, but SQLAlchemy telling it'll be Sequence.
    return db.scalars(stmt).all()

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