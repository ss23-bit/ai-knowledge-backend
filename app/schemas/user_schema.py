from pydantic import BaseModel, EmailStr
from _collections_abc import Sequence

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str

    # Allowed to create this model from a Python object's attributes, not just from a dictionary.
    model_config = {
        "from_attributes": True
    }

class UserUpdate(BaseModel):
    full_name: str

class UserListResponse(BaseModel):
    items: Sequence[UserResponse]
    total: int
    limit: int
    offset: int