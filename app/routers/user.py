"""
All routes for User
"""
from sqlalchemy.orm import Session
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

from app.database import get_db
from app.internal.auth import get_current_user
from app.internal.auth import get_password_hash
from app.internal.crud.user import crud_user
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserInDB
from app.schemas.user import UserOut
from app.schemas.user import UserUpdate

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", response_model=List[UserOut])
async def read_users(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_db)
) -> List[UserOut]:
    users = crud_user.get_multi(session, offset=offset, limit=limit)
    return users


@router.post("/", response_model=UserOut)
async def create_user(
    user_in: UserCreate, session: Session = Depends(get_db)
) -> UserOut:
    user = crud_user.get(session, username=user_in.username)
    if user is not None:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="The user with this username already exists in the system",
        )
    obj_in = UserInDB(
        **user_in.model_dump(), hashed_password=get_password_hash(user_in.password)
    )
    return crud_user.create(session, obj_in)


@router.get("/{user_id}/", response_model=UserOut)
async def read_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> UserOut:
    if current_user.id == user_id:
        return current_user

    user = crud_user.get(session, id=user_id)
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="The user doesn't have enough privileges"
        )
    if user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}/", response_model=UserOut)
async def update_user(
    user_id: int, user_in: UserUpdate, session: Session = Depends(get_db)
) -> UserOut:
    user = crud_user.get(session, id=user_id)
    if user is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist in the system",
        )
    try:
        user = crud_user.update(
            session,
            db_obj=user,
            obj_in={
                **user_in.model_dump(exclude={"password"}, exclude_none=True),
                "hashed_password": get_password_hash(user_in.password),
            },
        )
    except IntegrityError:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT, detail="User with this username already exits"
        )
    return user


@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    user = crud_user.get(session, id=user_id)
    if user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    if current_user.id == user_id:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="User can't delete itself")
    crud_user.delete(session, db_obj=user)
