from app.internal.crud.base import CRUDBase
from app.models.role import Role
from app.schemas.role import RoleInDB, RoleUpdateDB

CRUDRole = CRUDBase[Role, RoleInDB, RoleUpdateDB]
crud_role = CRUDBase(Role)
