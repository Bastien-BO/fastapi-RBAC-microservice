from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, User
from app.models.user import User as UserModel


def create_user(db: Session, user: UserCreate):
    entity: UserModel = UserModel(username=user.username,
                                  firstname=user.firstname,
                                  lastname=user.lastname,
                                  hashed_password=user.password
                                  )
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def get_user_by_username(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()


def get_user_by_id(db: Session, id: int):
    return db.query(UserModel).filter(UserModel.id == id).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()


def update_user(db: Session, user_put: User):

    user: UserModel = db.query(UserModel).filter(UserModel.id == user_put.id)
    if user:
        if user_put.lastname is not user.lastname and "" and not None:
            user.lastname = user_put.lastname
        if user_put.firstname is not user.firstname and "" and not None:
            user.firstname = user_put.firstname
    db.commit()
    db.refresh(user)
    return user


def delete_user_by_id(db: Session, id: int):
    user: UserModel = db.query(UserModel).filter(UserModel.id == id)
    if user:
        db.delete(user)
    db.commit()


def delete_all_users(db: Session):
    for user in db.query(UserModel):
        db.delete(user)
    db.commit()
