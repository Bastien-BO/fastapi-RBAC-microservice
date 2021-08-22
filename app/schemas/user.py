from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    firstname: str
    lastname: str
    username: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    is_active: bool = True
    hashed_password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserUpdateDB(UserBase):
    hashed_password: str
