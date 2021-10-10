import logging
from typing import List

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.internal.crud.permission import crud_permission
from app.schemas.permission import PermissionCreate
from app.settings import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_crud_permissions(session: Session, basic_permission_list: List[str]) -> None:
    crud_list: List[str] = ["create", "read", "update", "delete"]
    for crud in crud_list:
        for permission in basic_permission_list:
            perm: PermissionCreate = PermissionCreate(name=crud + "_" + permission)
            print(perm)
            if not crud_permission.get(session=session, name="test"):  # soucis ici
                print(perm)
                crud_permission.create(session=session, obj_in=perm)
                logger.info("Permission" + crud + "_" + permission + " created!")


def main() -> None:
    logger.info("Creating inital data")
    with SessionLocal() as session:
        add_crud_permissions(session=session, basic_permission_list=["permission"])
    logger.info("Initial data created")


if __name__ == "__main__":
    # get_settings()
    main()
