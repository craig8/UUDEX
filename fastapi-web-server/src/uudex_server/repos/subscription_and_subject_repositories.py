from typing import Awaitable
from sqlmodel import Session, select
import uudex_server.models as m
from uudex_server.repos import Repository


class SubscriptionRepository(Repository[m.Subscription]):

    def __init__(self, session: Session):
        super().__init__(m.Subscription, session=session, id_field="subscription_id")

    async def select_user_subscriptions(self, session: Session,
                                        user: m.AuthenticatedUser) -> list[m.Subscription]:
        statement = select(
            m.Subscription).where(m.Subscription.owner_endpoint_id == user.endpoint.endpoint_id)
        res = session.exec(statement=statement)
        return list(res)

    async def select_admin_subscriptions(self, session: Session) -> list[m.Subscription]:
        raise NotImplemented("This needs to be implemented better!")
        statement = select(Subscription)
        res = session.exec(statement=statement)
        return list(res)

    async def select_subscription_by_uuid(self, session: Session,
                                          subscription_uuid: str) -> m.Subscription | None:
        statement = select(
            m.Subscription).where(m.Subscription.subscription_uuid == subscription_uuid)
        res = session.exec(statement=statement)
        return res.first()


class SubscriptionSubjectRepository(Repository[m.SubscriptionSubject]):

    def __init__(self, session: Session):
        super().__init__(m.SubscriptionSubject,
                         session=session,
                         id_field="subscription_subject_id")

    async def select_subjects_by_subscription_uuid(
            self, session: Session, subscription_uuid: str) -> list[m.SubscriptionSubject]:
        statement = select(m.SubscriptionSubject).join(m.Subscription, isouter=True).where(
            m.Subscription.subscription_uuid == subscription_uuid
        )    #.where(SubscriptionSubject.subscription.subscription_uuid == subscription_uuid)
        res = session.exec(statement=statement)
        return list(res)

    async def select_subject_by_id(self, session: Session,
                                   subject_id: int) -> Awaitable[m.Subject] | None:
        statement = select(m.Subject).where(m.Subject.subject_id == subject_id)
        res = session.exec(statement=statement)
        return res.first()    # type: ignore


class SubjectRepository(Repository[m.Subject]):

    def __init__(self, session: Session):
        super().__init__(m.Subject, session=session, id_field="subject_id")


if __name__ == '__main__':

    async def main():
        from uudex_server.core.settings import get_settings
        from uudex_server.services.database_service import get_db_session

        settings = get_settings(".env-develop")
        session = get_db_session()
        endpoints = select_all_subjects(session=session)
        print("LIST")
        for endpoint in endpoints:
            print(endpoint.model_dump_json())
        print("END LIST")

        item = await select_subject_by_id(session=session,
                                          subject_id=endpoints[0].subject_id)    # type: ignore
        print("SINGLE SELECT")
        print(item)
        print("END SINGLE SELECT")

    import asyncio
    asyncio.run(main())
