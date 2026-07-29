from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from app.services.user_service import register_user, find_user_by_id, list_users, update_user_name, delete_user_by_id

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

@router.get(
        "",
        response_model=List[UserResponse],
)

def get_users(
    db: Session = Depends(get_db)
):

    # If collection resource is empty it'll return [] because it exist, unlike /users/1 that return None
    return list_users(
        db=db
    )

@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user_endpoint(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
):

    user = update_user_name(
        db=db,
        user_id=user_id,
        full_name=data.full_name,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db)
):

    success = delete_user_by_id(
        db=db,
        user_id=user_id,
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Response lets us control HTTP response.
    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )