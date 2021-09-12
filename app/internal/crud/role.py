from app.internal.crud.base import CRUDBase
from app.models.role import Role as RoleModel
from app.schemas.role import RoleUpdate, RoleCreate

CRUDRole = CRUDBase[RoleModel, RoleCreate, RoleUpdate]
crud_role = CRUDBase(RoleModel)
