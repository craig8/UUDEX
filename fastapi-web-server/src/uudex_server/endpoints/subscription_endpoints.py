from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session
from uudex_server.models import Subscription
from uudex_server.models.subscription_models import SubscriptionCreate
from uudex_server.models.subscription_subject_models import SubscriptionSubject
from uudex_server.services.database_service import get_db
from uudex_server.services.authentication_service import get_request_user
from uudex_server.models.authenticated_user import AuthenticatedUser
from uudex_server.repos import subscription_and_subject_repositories as ssr
from uudex_server.core.dependencies import SessionDep, UserDep

subscriptions_router = APIRouter(prefix="/subscriptions")
subscription_router = APIRouter(prefix="/subscription")

# Create v1 parent router
v1_router = APIRouter(prefix="/v1", tags=["v1"])
v1_router.include_router(subscriptions_router, tags=["v1", "subscriptions"])
v1_router.include_router(subscription_router, tags=["v1", "subscriptions"])


@subscription_router.get("/{subscription_uuid}/subjects")
async def get_subscription_subjects(subscription_uuid: str, session: SessionDep,
                                    user: UserDep) -> list[SubscriptionSubject]:

    repo = ssr.SubscriptionSubjectRepository(session)
    subscription_subjects: list[
        SubscriptionSubject] = await repo.select_subjects_by_subscription_uuid(
            session=session, subscription_uuid=subscription_uuid)

    if not user.is_admin():
        subscription_subjects = [
            sub for sub in subscription_subjects
            if sub.subscription.owner_endpoint_id == user.endpoint.endpoint_id
        ]

    return subscription_subjects


@subscriptions_router.get("/admin", operation_id="get_admin_subscriptions")
async def get_admin_subscriptions(session: SessionDep, user: UserDep) -> list[Subscription]:
    repo = ssr.SubscriptionRepository(session)
    return await repo.select_admin_subscriptions()


@subscriptions_router.get("/", operation_id="get_user_subscriptions")
async def get_user_subscriptions(session: SessionDep, user: UserDep) -> list[Subscription]:
    repo = ssr.SubscriptionRepository(session)
    return await repo.select_user_subscriptions(user=user)


@subscription_router.post("/", operation_id="create_subscription")
async def create_subscription(subscription: SubscriptionCreate, session: SessionDep,
                              user: UserDep) -> Subscription:
    # TODO: Implement create_subscription method in repository
    # For now, use a direct creation approach
    sub: Subscription = await ssr.create_subscription(session=session,
                                                      user=user,
                                                      subscription_add=subscription)
    return sub


@subscription_router.get("/{subscription_uuid}", operation_id="get_subscription_by_uuid")
async def get_subscription_by_uuid(subscription_uuid: str, session: SessionDep) -> Subscription:
    repo = ssr.SubscriptionRepository(session)
    sub: Subscription | None = await repo.select_subscription_by_uuid(
        subscription_uuid=subscription_uuid)
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    return sub
