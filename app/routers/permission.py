from typing import List

from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse
from requests import Session

from app.db_config import get_db
from app.internal.crud.permission import get_permission_by_id, get_all_permissions
from app.schemas.permission import Permission, PermissionCreate

router = APIRouter(
    prefix="/permission",
    tags=["permission"],
    responses={404: {"description": "not found"}},
)


@router.get("/all", response_model=List[Permission])
def get_permissions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_permissions(db=db, skip=skip, limit=limit)


@router.get("/{idi}", response_model=Permission)
def get_permission(idi: int, db: Session = Depends(get_db)):
    return get_permission_by_id(db=db, id=idi)


@router.post("", response_model=Permission)
def post_permission(permission: PermissionCreate):
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="")


@router.put("{id}", response_model=Permission)
def put_permission(id: int):
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content="")


@router.delete("/all", response_model=Permission)
def delete_permissions():
    return JSONResponse(status_code=status.HTTP_200_OK)


@router.delete("{id}", response_model=Permission)
def delete_permission(id: int):
    return JSONResponse(status_code=status.HTTP_200_OK)
