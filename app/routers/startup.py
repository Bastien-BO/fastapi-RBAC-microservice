"""
Startup Route
"""
from fastapi import APIRouter

router = APIRouter()


@router.on_event("startup")
def startup():
    pass  # add startup functions here
