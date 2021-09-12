import logging
from typing import List

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.internal.crud.permission import crud_permission
from app.schemas.permission import PermissionCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_crud_permissions(session: Session, basic_permission_list: List[str]) -> None:
    crud_list: List[str] = ["create", "read", "update", "delete"]
    for crud in crud_list:
        for permission in basic_permission_list:
            perm: PermissionCreate = PermissionCreate(name=crud + "_" + permission)
            if not crud_permission.get(session=session, name=permission):  # soucis ici
                print(perm)
                crud_permission.create(session=session, obj_in=perm)
                logger.info("Permission" + crud + "_" + permission + " created!")


def add_base_user(session: Session, role: str) -> None:
    pass


def main() -> None:
    logger.info("Creating inital data")
    with SessionLocal() as session:
        add_crud_permissions(session=session, basic_permission_list=["permission", "", ""])
        add_base_user(session=session, role="super_admin")
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
