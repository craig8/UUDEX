from fastapi import APIRouter, Depends, Request
from uudex_server.services.database_service import get_db_session
from uudex_server.models import EndPoint
import uudex_server.repos.endpoint_repository as ep

endpoint_router = APIRouter(prefix="/endpoint")


@endpoint_router.get("/me")
async def get_endpoint_user(request: Request) -> EndPoint:
    return request.state.endpoint
