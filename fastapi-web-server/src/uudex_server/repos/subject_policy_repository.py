from typing import Awaitable
from sqlmodel import Session, select
from uudex_server.models import SubjectPolicy


def select_all_subject_policy(session: Session) -> list[SubjectPolicy]:
    statement = select(SubjectPolicy)
    res = session.exec(statement=statement)
    return list(res)


async def select_subject_policy_id(session: Session,
                                   subject_policy_id: int) -> Awaitable[SubjectPolicy] | None:
    statement = select(SubjectPolicy).where(SubjectPolicy.subject_policy_id == subject_policy_id)
    res = session.exec(statement=statement)
    return res.first()    # type: ignore


if __name__ == '__main__':

    async def main():
        from uudex_server.core.settings import get_settings
        from uudex_server.services.database_service import get_db_session

        settings = get_settings(".env-develop")
        session = get_db_session()
        endpoints = select_all_subject_policy(session=session)
        print("LIST")
        for endpoint in endpoints:
            print(endpoint.model_dump_json())
        print("END LIST")

        item = await select_subject_policy_id(session=session,
                                              subject_policy_id=endpoints[0].subject_policy_id
                                              )    # type: ignore
        print("SINGLE SELECT")
        print(item)
        print("END SINGLE SELECT")

    import asyncio
    asyncio.run(main())
