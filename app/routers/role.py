from typing import List

from fastapi import status, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db_config import get_db
from app.internal.crud.role import get_all_roles, get_role_by_id, get_role_by_name, create_role, delete_all_roles, \
    update_role
from app.schemas.role import Role, RoleCreate

router = APIRouter(
    prefix="/role",
    tags=["role"],
    responses={404: {"description": "not found"}},
)


@router.get("/all", response_model=List[Role])
def get_role(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_roles(db=db, skip=skip, limit=limit)


@router.get("/{id}", response_model=Role)
def get_role(id: int, db: Session = Depends(get_db)):
    role_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"could not find role: {id}",
    )
    role = get_role_by_id(db=db, id=id)

    if role:
        return role
    else:
        raise role_exception


@router.post("", response_model=Role)
def post_permission(role: RoleCreate, db: Session = Depends(get_db)):
    role_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"role {role.name} already exist",
    )
    role_db = get_role_by_name(db=db, name=role.name)

    if role_db:
        return role_exception
    else:
        return create_role(db=db, role=role)


@router.put("{id}", response_model=Role)
def put_role(id: int, db: Session = Depends(get_db)):
    db_role: Role = get_role_by_id(db=db, id=id)
    if not db_role:
        raise HTTPException(status_code=400, detail=f"role {db_role.name} already exist")
    else:
        return update_role(db=db, role_put=db_role)


@router.delete("/all", response_model=Role)
def delete_role(db: Session = Depends(get_db)):
    delete_all_roles(db=db)


@router.delete("{id}", response_model=Role)
def delete_role(id: int, db: Session = Depends(get_db)):
    role_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"could not find role: {id}",
    )
    role = get_role_by_id(db=db, id=id)
    if role:
        return delete_role(db=db, id=id)
    else:
        raise role_exception
