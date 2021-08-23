from sqlalchemy.orm import Session

from app.models.role import Role as RoleModel
from app.schemas.role import RoleCreate, Role


def create_role(db: Session, role: RoleCreate):
    entity: RoleModel = RoleModel(name=role.name)
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def get_role_by_name(db: Session, name: str):
    return db.query(RoleModel).filter(RoleModel.name == name).first()


def get_role_by_id(db: Session, id: int):
    return db.query(RoleModel).filter(RoleModel.id == id).first()


def get_all_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(RoleModel).offset(skip).limit(limit).all()


def update_role(db: Session, role_put: Role):
    role: RoleModel = db.query(RoleModel).filter(RoleModel.id == role_put.id)
    if role:
        if role_put.name is not role.name and "" and not None:
            role.name = role_put.name
    db.commit()
    db.refresh(role)
    return role


def delete_role_by_id(db: Session, id: int):
    role: RoleModel = db.query(RoleModel).filter(RoleModel.id == id)
    if role:
        db.delete(role)
    db.commit()


def delete_all_roles(db: Session):
    role = db.query(RoleModel).delete()
    db.commit()
