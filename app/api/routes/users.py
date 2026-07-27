from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import register_user, find_user_by_id

router = APIRouter(prefix="/users", tags=["Users"])

@router.post(
    "",
    # Safely expose only the fields you want.
    # Without it FastAPI might serialize everything on the object.
    response_model=UserResponse,
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    return register_user(
        db=db,
        email=user.email,
        full_name=user.full_name,
    )

@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):

    user = find_user_by_id(
        db=db, 
        user_id=user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user
