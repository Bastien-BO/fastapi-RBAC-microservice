from typing import List

from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db_config import get_db
from app.internal.auth import get_current_active_user
from app.internal.user import get_user_by_id, get_all_users, create_user, delete_all_users, update_user, \
    delete_user_by_id, get_user_by_username
from app.schemas.user import User, UserCreate

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "not found"}},
)


@router.get("/all", response_model=List[User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_users(db=db, skip=skip, limit=limit)


@router.get("/{id}", response_model=User)
def get_user(id: int, db: Session = Depends(get_db)):
    user_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"could not find job: {id}",
    )
    user = get_user_by_id(db=db, id=id)
    if user:
        return user
    else:
        raise user_exception


@router.post("", response_model=User)
def post_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User aleready registered")
    else:
        return create_user(db=db, user=user)


@router.put("{id}", response_model=User)
def put_user(user: User, db: Session = Depends(get_db)):
    return update_user(db=db, user_put=user)


@router.delete("{id}", response_model=User)
def delete_user(id: int, db: Session = Depends(get_db)):
    delete_user_by_id(id=id, db=db)
    return JSONResponse(status_code=status.HTTP_200_OK)


@router.delete("/all", response_model=User)
def delete_users(db: Session = Depends(get_db)):
    delete_all_users(db=db)
    return JSONResponse(status_code=status.HTTP_200_OK)


@router.get("/me", response_model=User)
def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.put("/{id}/deactivate", response_model=User)
def deactivate_user(id: int, db: Session = Depends(get_db)):
    db_user: User = get_user_by_id(db=db, id=id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User do not exist")
    else:
        db_user.is_active = False
        return update_user(db=db, user_put=db_user)


@router.put("/{id}/activate", response_model=User)
def deactivate_user(id: int, db: Session = Depends(get_db)):
    db_user: User = get_user_by_id(db=db, id=id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User do not exist")
    else:
        db_user.is_active = True
        return update_user(db=db, user_put=db_user)
