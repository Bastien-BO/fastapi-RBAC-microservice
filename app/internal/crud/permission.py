from app.internal.crud.base import CRUDBase
from app.models.permission import Permission
from app.schemas.permission import PermissionInDB, PermissionUpdateDB

CRUDPermission = CRUDBase[Permission, PermissionInDB, PermissionUpdateDB]
crud_permission = CRUDBase(Permission)
