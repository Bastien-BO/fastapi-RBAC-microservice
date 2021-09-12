from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True
