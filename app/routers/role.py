from typing import List

from fastapi import status, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.internal.crud.role import crud_role
from app.schemas.role import Role, RoleCreate, RoleUpdate

router = APIRouter(
    prefix="/role",
    tags=["role"],
    responses={404: {"description": "not found"}},
)


@router.get("/", response_model=List[Role])
def get_role(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_role.get_multi(session=db, offset=skip, limit=limit)


@router.get("/{id_role}", response_model=Role)
def get_role(id_role: int, db: Session = Depends(get_db)):
    role_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"could not find role: {id_role}",
    )
    role = crud_role.get(session=db, id=id_role)

    if role:
        return role
    else:
        raise role_exception


@router.post("/", response_model=Role)
def post_permission(role: RoleCreate, db: Session = Depends(get_db)):
    role_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"role {role.name} already exist",
    )
    role_db = crud_role.get(session=db, name=role.name)

    if role_db:
        return role_exception
    else:
        return crud_role.create(session=db, role=role)


@router.put("/{id_role}", response_model=Role)
def put_role(id_role: int, role_in: RoleUpdate, db: Session = Depends(get_db)):
    db_role: Role = crud_role.get(session=db, id=id_role)

    if not db_role:
        raise HTTPException(status_code=400, detail=f"role {db_role.name} do not exist")
    else:
        return crud_role.update(session=db, db_obj=db_role, obj_in=role_in)


@router.delete("/{id_role}", response_model=Role)
def delete_role(id_role: int, db: Session = Depends(get_db)):
    role_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"could not find role: {id_role}",
    )
    role = crud_role.get(session=db, id=id_role)

    if role:
        return crud_role.delete(session=db,db_obj=role)
    else:
        raise role_exception
