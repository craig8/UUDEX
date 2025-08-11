"""
Example of how to use the authentication dependencies in FastAPI endpoints.
This demonstrates the clean pattern for replacing Flask decorators with FastAPI dependencies.
"""
from fastapi import APIRouter, Depends
from uudex_server.core.dependencies import CurrentUserDep, AdminUserDep, ParticipantAdminUserDep
from uudex_server.models.authenticated_user import AuthenticatedUser

router = APIRouter()


@router.get("/protected")
async def protected_endpoint(current_user: CurrentUserDep):
    """
    Any authenticated user can access this endpoint.
    Equivalent to Flask's @authenticate_session decorator.
    """
    return {
        "message": "You are authenticated",
        "endpoint_id": current_user.endpoint.endpoint_id,
        "participant_id": current_user.endpoint.participant_id,
        "is_admin": current_user.is_admin(),
        "is_participant_admin": current_user.is_participant_admin()
    }


@router.get("/admin-only")
async def admin_only_endpoint(admin_user: AdminUserDep):
    """
    Only UUDEX administrators can access this endpoint.
    Equivalent to Flask's @authenticate_session + admin check.
    """
    return {
        "message": "You are a UUDEX administrator",
        "endpoint_id": admin_user.endpoint.endpoint_id
    }


@router.get("/participant-admin-only")
async def participant_admin_only_endpoint(participant_admin: ParticipantAdminUserDep):
    """
    Only participant administrators can access this endpoint.
    """
    return {
        "message": "You are a participant administrator",
        "endpoint_id": participant_admin.endpoint.endpoint_id,
        "participant_id": participant_admin.endpoint.participant_id
    }


@router.get("/flexible-auth")
async def flexible_auth_endpoint(current_user: CurrentUserDep):
    """
    Custom logic based on user roles.
    You can access all the same information as in Flask's g object.
    """
    response = {
        "endpoint_id": current_user.endpoint.endpoint_id,
        "endpoint_uuid": current_user.endpoint.endpoint_uuid,
        "participant_id": current_user.endpoint.participant_id,
        "user_name": current_user.endpoint.endpoint_user_name,
        "roles": {
            "uudex_admin": current_user.is_admin(),
            "participant_admin": current_user.is_participant_admin()
        }
    }

    # Custom logic based on roles
    if current_user.is_admin():
        response["admin_data"] = "Secret admin information"
    elif current_user.is_participant_admin():
        response["participant_data"] = "Participant-specific data"

    return response
