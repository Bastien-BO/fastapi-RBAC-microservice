from fastapi import APIRouter

router = APIRouter(
    tags=["base"],
    responses={404: {"description": "not found"}},
)


@router.get('/')
def hello_world():
    return {'message': 'Hello, World!'}
