from typing import List

from pydantic import BaseModel

from app.schemas.role import Role


class PermissionBase(BaseModel):
    name: str


class PermissionCreate(PermissionBase):
    roles: List[Role] = []


class PermissionUpdate(PermissionBase):
    roles: List[Role] = []


class Permission(PermissionBase):
    id: int
    roles: List[Role] = []

    class Config:
        orm_mode = True
