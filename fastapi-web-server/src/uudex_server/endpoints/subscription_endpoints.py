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

subscriptions_router = APIRouter(prefix="/subscriptions")
subscription_router = APIRouter(prefix="/subscription")


@subscription_router.get("/{subscription_uuid}/subjects")
async def get_subscription_subjects(
    subscription_uuid: str,
    session: AsyncSession = Depends(get_db),
    user: AuthenticatedUser = Depends(get_request_user)
) -> list[SubscriptionSubject]:

    repo = ssr.SubscriptionSubjectRepository(session)
    subscription_subjects: list[
        SubscriptionSubject] = await repo.select_subjects_by_subscription_uuid(
            subscription_uuid=subscription_uuid)

    if not user.is_admin():
        subscription_subjects = [
            sub for sub in subscription_subjects
            if sub.subscription.owner_endpoint_id == user.endpoint.endpoint_id
        ]

    return subscription_subjects


@subscriptions_router.get("/admin", operation_id="get_admin_subscriptions")
async def get_admin_subscriptions(session: AsyncSession = Depends(get_db),
                                  user: AuthenticatedUser = Depends(
                                      get_request_user)) -> list[Subscription]:
    repo = ssr.SubscriptionRepository(session)
    return await repo.select_admin_subscriptions()


@subscriptions_router.get("/", operation_id="get_user_subscriptions")
async def get_user_subscriptions(session: AsyncSession = Depends(get_db),
                                 user: AuthenticatedUser = Depends(
                                     get_request_user)) -> list[Subscription]:
    repo = ssr.SubscriptionRepository(session)
    return await repo.select_user_subscriptions(user=user)


@subscription_router.post("/", operation_id="create_subscription")
async def create_subscription(
    subscription: SubscriptionCreate,
    session: AsyncSession = Depends(get_db),
    user: AuthenticatedUser = Depends(get_request_user)
) -> Subscription:
    repo = ssr.SubscriptionRepository(session)
    sub: Subscription = await repo.create_subscription(user=user, subscription_add=subscription)
    return sub


@subscription_router.get("/{subscription_uuid}", operation_id="get_subscription_by_uuid")
async def get_subscription_by_uuid(
    subscription_uuid: str, session: AsyncSession = Depends(get_db)) -> Subscription:
    repo = ssr.SubscriptionRepository(session)
    sub: Subscription = await repo.select_subscription_by_uuid(subscription_uuid=subscription_uuid)
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    return sub
