from pydantic import BaseModel


class PermissionBase(BaseModel):
    name: str


class PermissionCreate(PermissionBase):
    pass


class PermissionOut(PermissionBase):
    id: int

    class Config:
        orm_mode = True


class PermissionInDB(PermissionBase):
    pass


class PermissionUpdate(PermissionBase):
    pass


class PermissionUpdateDB(PermissionBase):
    pass
