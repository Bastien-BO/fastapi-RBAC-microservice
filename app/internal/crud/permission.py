from app.internal.crud.base import CRUDBase
from app.models.permission import Permission as PermissionModel
from app.schemas.permission import PermissionCreate, PermissionUpdate

CRUDPermission = CRUDBase[PermissionModel, PermissionCreate, PermissionUpdate]
crud_permission = CRUDBase(PermissionModel)
