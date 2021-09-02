from fastapi import APIRouter, status

router = APIRouter(
    tags=["healthcheck"],

    responses={404: {"description": "not found"}},
)


@router.get('/healthcheck', status_code=status.HTTP_200_OK)
def perform_healthcheck_heroku():
    """
    Simple route for the GitHub Actions to healthcheck on.
    More info is available at:
    https://github.com/akhileshns/heroku-deploy#health-check
    It basically sends a GET request to the route & hopes to get a "200"
    response code. Failing to return a 200 response code just enables
    the GitHub Actions to rollback to the last version the project was
    found in a "working condition". It acts as a last line of defense in
    case something goes south.
    Additionally, it also returns a JSON response in the form of:
    {
      'healtcheck': 'Everything OK!'
    }
    """
    return {'healthcheck': 'Everything OK!'}
