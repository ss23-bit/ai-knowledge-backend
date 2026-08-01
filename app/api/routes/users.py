from fastapi import APIRouter, Depends, HTTPException, Response, status, Query
from sqlalchemy.orm import Session
from typing import List, Annotated

from app.api.dependencies import get_db
from app.schemas.user_schema import (
    UserCreate, 
    UserResponse, 
    UserUpdate, 
    UserListResponse,
)
from app.services.user_service import (
    register_user, 
    find_user_by_id, 
    list_users, 
    update_user_name, 
    delete_user_by_id,
)

router = APIRouter(prefix="/users", tags=["Users"])

def user_not_found():
    raise HTTPException(
                status_code=404,
                detail="User not found"
            )

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
        user_not_found()

    return user

@router.get(
        "",
        response_model=UserListResponse,
)

def get_users(
    # limit, offset and search is Query Parameter. It's not in the url path and not pydantic model, so FastAPI assume it is QP. 
    # Annotated attaching extra metadata. "Annotated[TYPE, EXTRA_INFORMATION]"
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    # = None making Search Optional without it there's no default value and it will raise an error because python required a value.
    search: str | None = None,
    sort: str | None = None,
    db: Session = Depends(get_db),
):
    try:
        users, total = list_users(
            db=db,
            limit=limit,
            offset=offset,
            search=search,
            sort=sort,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=e,
        )

    # The API response object, it includes metadata.
    return {
        "items": users,
        "total": total,
        "limit": limit,
        "offset": offset,
    }

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
        user_not_found()

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