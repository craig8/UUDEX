from fastapi import APIRouter, Depends, Request
from uudex_server.services.database_service import get_db_session
from uudex_server.models import EndPoint
from uudex_server.core.dependencies import CurrentUserDep
import uudex_server.repos.endpoint_repository as ep

endpoint_router = APIRouter(prefix="/endpoint")

# Create v1 parent router
v1_router = APIRouter(prefix="/v1", tags=["v1"])
v1_router.include_router(endpoint_router, tags=["v1", "endpoints"])


@endpoint_router.get("/me")
async def get_endpoint_user(current_user: CurrentUserDep) -> EndPoint:
    """
    Get the current authenticated user's endpoint information.
    Uses the authentication dependency to return the endpoint data.
    """
    return current_user.endpoint
