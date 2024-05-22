from typing import Awaitable
from sqlmodel import Session, select
from uudex_server.models import Subscription, SubscriptionAdd
from uudex_server.models.authenticated_user import AuthenticatedUser


async def select_user_subscriptions(session: Session,
                                    user: AuthenticatedUser) -> list[Subscription]:
    statement = select(Subscription).where(
        Subscription.owner_endpoint_id == user.endpoint.endpoint_id)
    res = session.exec(statement=statement)
    return list(res)


async def select_admin_subscriptions(session: Session) -> list[Subscription]:
    statement = select(Subscription)
    res = session.exec(statement=statement)
    return list(res)


async def select_subscription_by_uuid(session: Session,
                                      subscription_uuid: str) -> Subscription | None:
    statement = select(Subscription).where(Subscription.subscription_uuid == subscription_uuid)
    res = session.exec(statement=statement)
    return res.first()


async def create_subscription(session: Session, user: AuthenticatedUser,
                              subscription_add: SubscriptionAdd) -> Subscription:
    subscription = Subscription(**subscription_add.dict(),
                                owner_endpoint_id=user.endpoint.endpoint_id)
    #subscription.owner_endpoint_id = user.endpoint.endpoint_id
    session.add(subscription)
    session.commit()
    session.refresh(subscription)
    return subscription
