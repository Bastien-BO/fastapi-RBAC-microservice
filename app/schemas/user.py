from pydantic import BaseModel


class UserBase(BaseModel):
    firstname: str
    lastname: str
    role_id: int
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class UserVerify(UserBase):
    id: int
    is_active: bool
    hashed_password: str

    class Config:
        orm_mode = True
