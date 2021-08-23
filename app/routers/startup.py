import os

from fastapi import APIRouter
from sqlalchemy.orm import Session, sessionmaker

from app.database import engine
from app.internal.crud.permission import add_basic_permission
from app.settings import get_settings

router = APIRouter()


@router.on_event("startup")
def startup():
    new_sessionmaker: sessionmaker = sessionmaker(bind=engine)
    session: Session = new_sessionmaker()
    add_basic_permission(db=session)
