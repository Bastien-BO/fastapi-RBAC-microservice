"""
Health route
"""
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi_health import health

from app.internal.health import healthy_condition
from app.internal.health import sick_condition

router = APIRouter(
    tags=["healthcheck"],
)


@router.get("/health", status_code=status.HTTP_200_OK)
def perform_api_healthcheck(
    health_endpoint=Depends(health([healthy_condition, sick_condition]))
):
    return health_endpoint
