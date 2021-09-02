from fastapi import APIRouter, status, Depends
from fastapi_health import health

from app.internal.health import healthy_condition, sick_condition

router = APIRouter(
    tags=["healthcheck"],
    responses={404: {"description": "not found"}},
)


@router.get('/health', status_code=status.HTTP_200_OK)
def perform_healthcheck_of_api(health_endpoint=Depends(health([healthy_condition, sick_condition]))):
    return health_endpoint
