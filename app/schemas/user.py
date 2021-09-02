from typing import Optional, List

from pydantic import BaseModel, EmailStr

from app.schemas.role import RoleOut


class UserBase(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    is_active: bool = True
    hashed_password: str


class UserUpdate(UserBase):
    password: Optional[str] = None
    roles: List[RoleOut]


class UserUpdateDB(UserBase):
    hashed_password: str
