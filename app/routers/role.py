"""
All routes for Role
"""
from typing import List

from fastapi import status
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from app.database import get_db
from app.internal.crud.role import crud_role
from app.schemas.role import Role
from app.schemas.role import RoleCreate
from app.schemas.role import RoleUpdate

router = APIRouter(
    prefix="/role",
    tags=["role"],
)


@router.get("/", response_model=List[Role])
def get_role(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[Role]:
    """
    Create Roles
    """
    return crud_role.get_multi(session=db, offset=skip, limit=limit)


@router.get("/{id_role}", response_model=Role)
def get_role(id_role: int, db: Session = Depends(get_db)) -> Role:
    """
    Get a Role
    """
    role = crud_role.get(session=db, id=id_role)

    if role:
        return role
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, f"could not find role: {id_role}")


@router.post("/", response_model=Role)
def post_permission(role: RoleCreate, db: Session = Depends(get_db)) -> Role:
    """
    Create a Role
    """
    role_db = crud_role.get(session=db, name=role.name)
    if role_db:
        raise HTTPException(HTTP_404_NOT_FOUND, f"role {role.name} already exist")
    else:
        return crud_role.create(session=db, obj_in=role)


@router.patch("/{id_role}", response_model=Role)
def update_role(
    id_role: int, role_in: RoleUpdate, db: Session = Depends(get_db)
) -> Role:
    """
    Update a Role
    """
    db_role: Role = crud_role.get(session=db, id=id_role)
    if not db_role:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"role {db_role.name} do not exist"
        )
    else:
        return crud_role.update(session=db, db_obj=db_role, obj_in=role_in)


@router.delete("/{id_role}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    id_role: int, db: Session = Depends(get_db)
):
    """
    Delete a Role
    """
    role = crud_role.get(session=db, id=id_role)

    if role:
        crud_role.delete(session=db, db_obj=role)
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, f"could not find role: {id_role}")
