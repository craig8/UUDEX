from typing import Awaitable
from sqlmodel import Session, select
from uudex_server.models import Subscription, SubscriptionCreate
from uudex_server.models.authenticated_user import AuthenticatedUser

from sqlmodel import Session, select, delete
from uudex_server.models import Subscription, SubscriptionCreate, SubscriptionDelete

from uudex_server.models.subscription_models import Subscription
from uudex_server.repos import Repository


class SubscriptionRepository(Repository[Subscription]):

    def __init__(self):
        super().__init__(Subscription, id_field="subscription_id")

    async def select_user_subscriptions(self, session: Session,
                                        user: AuthenticatedUser) -> list[Subscription]:
        statement = select(Subscription).where(
            Subscription.owner_endpoint_id == user.endpoint.endpoint_id)
        res = session.exec(statement=statement)
        return list(res)

    async def select_admin_subscriptions(self, session: Session) -> list[Subscription]:
        raise NotImplemented("This needs to be implemented better!")
        statement = select(Subscription)
        res = session.exec(statement=statement)
        return list(res)

    async def select_subscription_by_uuid(self, session: Session,
                                          subscription_uuid: str) -> Subscription | None:
        statement = select(Subscription).where(Subscription.subscription_uuid == subscription_uuid)
        res = session.exec(statement=statement)
        return res.first()
