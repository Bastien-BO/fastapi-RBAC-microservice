from app.internal.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserInDB, UserUpdateDB

CRUDUser = CRUDBase[User, UserInDB, UserUpdateDB]
crud_user = CRUDBase(User)