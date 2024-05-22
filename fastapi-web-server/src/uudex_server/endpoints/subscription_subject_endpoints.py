from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from uudex_server.models.subject_models import Subject
from uudex_server.models.subscription_models import Subscription, SubscriptionAdd
from uudex_server.services.database_service import get_db_session
from uudex_server.services.authentication_service import get_request_user
from uudex_server.models.authenticated_user import AuthenticatedUser
from uudex_server.repos import subscription_subject_repository as pr
from uudex_server.models.subscription_subject_models import SubscriptionSubject
from uudex_server.endpoints.subscription_endpoints import get_subscription_router


@get_subscription_router().get("/{subscription_uuid}/subjects")
async def get_subscription_subjects(
        subscription_uuid: str, session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[AuthenticatedUser,
                        Depends(get_request_user)]) -> list[SubscriptionSubject]:

    subscription_subjects: list[
        SubscriptionSubject] = await pr.select_subjects_by_subscription_uuid(
            session=session, subscription_uuid=subscription_uuid)
    return subscription_subjects
    # if not user.is_admin():
    #     pr.sel

    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    # subscriptions: list[Subscription] = await pr.select_admin_subscriptions(session=session, user=user)
    # return subscriptions
