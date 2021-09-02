from typing import List

from fastapi import status, APIRouter, Depends, HTTPException
from requests import Session

from app.database import get_db
from app.internal.crud.permission import crud_permission
from app.schemas.permission import PermissionCreate, PermissionOut, PermissionUpdate

router = APIRouter(
    prefix="/permission",
    tags=["permission"],
    responses={404: {"description": "not found"}},
)


@router.get("/", response_model=List[PermissionOut])
def get_permission(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_permission.get_multi(session=db, skip=skip, limit=limit)


@router.get("/{id_permission}", response_model=PermissionOut)
def get_permission(id_permission: int, db: Session = Depends(get_db)):
    permission_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"could not find Permission: {id_permission}",
    )
    permission = crud_permission.get(session=db, id=id_permission)

    if permission:
        return permission
    else:
        raise permission_exception


@router.post("/", response_model=PermissionOut)
def post_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    permission_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Permission {permission.name} already exist",
    )
    permission_db = crud_permission.get(session=db, name=permission.name)

    if permission_db:
        return permission_exception
    else:
        return crud_permission.create(session=db, Permission=permission)


@router.put("/{id_permission}", response_model=PermissionOut)
def put_permission(id_permission: int, permission_in: PermissionUpdate, db: Session = Depends(get_db)):
    db_permission: PermissionOut = crud_permission.get(session=db, id=id_permission)

    if not db_permission:
        raise HTTPException(status_code=400, detail=f"Permission {db_permission.name} do not exist")
    else:
        return crud_permission.update(session=db, db_obj=db_permission, obj_in=permission_in)


@router.delete("/{id_permission}", response_model=PermissionOut)
def delete_permission(id_permission: int, db: Session = Depends(get_db)):
    permission_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"could not find Permission: {id_permission}",
    )
    permission = crud_permission.get(session=db, id=id_permission)

    if permission:
        return crud_permission.delete(session=db, db_obj=permission)
    else:
        raise permission_exception
