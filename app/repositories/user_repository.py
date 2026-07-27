from sqlalchemy import select
from sqlalchemy.orm import Session

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