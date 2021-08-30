from sqlalchemy.orm import Session

from app.models.permission import Permission as PermissionModel
from app.schemas.permission import PermissionCreate


def create_permission(db: Session, permission: PermissionCreate):
    entity: PermissionModel = PermissionModel(name=permission.name)
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def get_permission_by_name(db: Session, name: str):
    return db.query(PermissionModel).filter(PermissionModel.name == name).first()


def get_permission_by_id(db: Session, id: int):
    return db.query(PermissionModel).filter(PermissionModel.id == id).first()


def get_all_permissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PermissionModel).offset(skip).limit(limit).all()


def add_basic_permission(db: Session):
    crud = ["get", "add", "delete", "put"]
    model = ["user", "role", "permission"]
    for x in range(0, len(crud)):
        for y in range(0, len(model)):
            permission = PermissionCreate(name=crud[x] + "_" + model[y])
            user = get_permission_by_name(db=db, name=crud[x] + "_" + model[y])
            if not user:
                create_permission(db=db, permission=permission)
