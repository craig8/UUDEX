from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from uudex_server.models.subscription_models import Subscription, SubscriptionAdd
from uudex_server.models.subscription_subject_models import SubscriptionSubject
from uudex_server.services.database_service import get_db_session
from uudex_server.services.authentication_service import get_request_user
from uudex_server.models.authenticated_user import AuthenticatedUser
from uudex_server.repos import subscription_repository as pr
from uudex_server.repos import subscription_subject_repository as pr_subject

subscriptions_router = APIRouter(prefix="/subscriptions")
subscription_router = APIRouter(prefix="/subscription")


@subscription_router.get("/{subscription_uuid}/subjects")
async def get_subscription_subjects(
        subscription_uuid: str, session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[AuthenticatedUser,
                        Depends(get_request_user)]) -> list[SubscriptionSubject]:

    subscription_subjects: list[
        SubscriptionSubject] = await pr_subject.select_subjects_by_subscription_uuid(
            session=session, subscription_uuid=subscription_uuid)

    if not user.is_admin():
        subscription_subjects = [
            sub for sub in subscription_subjects
            if sub.subscription.owner_endpoint_id == user.endpoint.endpoint_id
        ]

    return subscription_subjects


@subscriptions_router.get("/admin", operation_id="get_all_subscriptions")
async def get_all_subscriptions(
        session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[AuthenticatedUser, Depends(get_request_user)]) -> list[Subscription]:
    if not user.is_admin():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    subscriptions: list[Subscription] = await pr.select_admin_subscriptions(session=session,
                                                                            user=user)
    return subscriptions


@subscriptions_router.get("/", operation_id="get_user_subscriptions")
async def get_user_subscriptions(
        session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[AuthenticatedUser, Depends(get_request_user)]) -> list[Subscription]:
    subscriptions: list[Subscription] = await pr.select_user_subscriptions(session=session,
                                                                           user=user)
    return subscriptions


@subscription_router.post("/", operation_id="create_subscription")
async def create_subscription(
        subscription: SubscriptionAdd, session: Annotated[Session,
                                                          Depends(get_db_session)],
        user: Annotated[AuthenticatedUser, Depends(get_request_user)]) -> Subscription:
    sub: Subscription = await pr.create_subscription(session=session,
                                                     user=user,
                                                     subscription_add=subscription)
    return sub


@subscription_router.get("/{subscription_uuid}", operation_id="get_subscription")
async def get_subscription(
        subscription_uuid: str, session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[AuthenticatedUser, Depends(get_request_user)]) -> Subscription | None:
    sub: Subscription | None = await pr.select_subscription_by_uuid(
        session=session, subscription_uuid=subscription_uuid)
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    if sub.owner_endpoint_id != user.endpoint.endpoint_id and not (user.is_active()
                                                                   and user.is_admin()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    return sub
