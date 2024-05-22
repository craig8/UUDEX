from typing import Awaitable
from sqlmodel import Session, select
from uudex_server.models import Subject
from uudex_server.models.subscription_models import Subscription
from uudex_server.models.subscription_subject_models import SubscriptionSubject


async def select_subjects_by_subscription_uuid(
        session: Session, subscription_uuid: str) -> list[SubscriptionSubject]:
    statement = select(SubscriptionSubject).join(Subscription, isouter=True).where(
        Subscription.subscription_uuid == subscription_uuid
    )    #.where(SubscriptionSubject.subscription.subscription_uuid == subscription_uuid)
    res = session.exec(statement=statement)
    return list(res)


def select_all_subjects(session: Session) -> list[Subject]:
    statement = select(Subject)
    res = session.exec(statement=statement)
    return list(res)


async def select_subject_by_id(session: Session, subject_id: int) -> Awaitable[Subject] | None:
    statement = select(Subject).where(Subject.subject_id == subject_id)
    res = session.exec(statement=statement)
    return res.first()    # type: ignore


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
