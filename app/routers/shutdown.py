from fastapi import APIRouter

router = APIRouter()


@router.on_event("shutdown")
def shutdown():
    pass  # add shutdown functions here
