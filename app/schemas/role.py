from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleOut(RoleBase):
    id: int

    class Config:
        orm_mode = True


class RoleInDB(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleUpdateDB(RoleBase):
    pass
