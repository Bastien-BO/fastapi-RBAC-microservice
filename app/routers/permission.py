"""
All routes for Permissions
"""
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from requests import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.internal.crud.permission import crud_permission
from app.internal.crud.role import crud_role
from app.schemas.permission import Permission
from app.schemas.permission import PermissionCreate
from app.schemas.permission import PermissionUpdate

from app.schemas.role import Role

router = APIRouter(
    prefix="/permission",
    tags=["permission"],
)


@router.get("/", response_model=List[Permission])
def get_permission(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> Permission:
    return crud_permission.get_multi(session=db, offset=skip, limit=limit)


@router.get("/{id_permission}", response_model=Permission)
def get_permission(
    id_permission: int, db: Session = Depends(get_db)
) -> Permission:
    permission_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"could not find Permission: {id_permission}",
    )
    permission = crud_permission.get(session=db, id=id_permission)

    if permission:
        return permission
    else:
        raise permission_exception


@router.post("/", response_model=Permission)
def post_permission(
    permission: PermissionCreate, db: Session = Depends(get_db)
) -> Permission:
    permission_db = crud_permission.get(session=db, name=permission.name)

    if permission_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Permission {permission.name} already exist",
        )
    try:
        permission_create: PermissionCreate = PermissionCreate(
            name=permission.name
        )
        for nb in range(0, len(permission.roles)):
            role_found: Role = crud_role.get(
                session=db, id=permission.roles[nb].id
            )
            if role_found:
                permission_create.roles.append(role_found)
            else:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Unable to find role {permission.roles[nb].id}",
                )
        return crud_permission.create(session=db, obj_in=permission_create)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unable to create permission",
        )


@router.patch("/{id_permission}", response_model=Permission)
def update_permission(
    id_permission: int,
    permission_in: PermissionUpdate,
    db: Session = Depends(get_db),
) -> Permission:
    db_permission = crud_permission.get(session=db, id=id_permission)
    if db_permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Permission id:{id_permission} do not exist",
        )
    try:
        permission_update = PermissionUpdate(name=permission_in.name)
        for nb in range(0, len(permission_in.roles)):
            role_found = crud_role.get(
                session=db, id=permission_in.roles[nb].id
            )
            if role_found:
                permission_update.roles.append(role_found)
            else:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Unable to find role {permission_in.roles[nb].id}",
                )
        return crud_permission.update(
            session=db, db_obj=db_permission, obj_in=permission_update
        )
        # return crud_permission.create(session=db, obj_in=permission_create)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unable to update permission",
        )


@router.delete("/{id_permission}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(
    id_permission: int, db: Session = Depends(get_db)
) -> status.HTTP_204_NO_CONTENT:

    permission = crud_permission.get(session=db, id=id_permission)

    if permission:
        crud_permission.delete(session=db, db_obj=permission)
    else:
        raise HTTPException(
            404,
            f"could not find Permission: {id_permission}",
        )
