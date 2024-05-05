from typing import Awaitable
from sqlmodel import Session, select
from uudex_server.models import DataType


def select_all_data_types(session: Session) -> list[DataType]:
    statement = select(DataType)
    res = session.exec(statement=statement)
    return list(res)


async def select_by_data_type_id(session: Session,
                                 data_type_id: int) -> Awaitable[DataType] | None:
    statement = select(DataType).where(DataType.data_type_id == data_type_id)
    res = session.exec(statement=statement)
    return res.first()    # type: ignore


if __name__ == '__main__':

    async def main():

        from uudex_server.core.settings import get_settings
        from uudex_server.services.database_service import get_db_session

        settings = get_settings(".env-develop")
        session = get_db_session()
        endpoints = select_all_data_types(session=session)
        print("LIST")
        for endpoint in endpoints:
            print(endpoint.model_dump_json())
        print("END LIST")
        # item = await select_by_data_type_id(session=session,
        #                                           data_type_id=endpoints[0].data_type_id
        #                                           )    # type: ignore
        # print("SINGLE SELECT")
        # print(item)
        # print("END SINGLE SELECT")

        item = await select_by_data_type_id(session=session,
                                            data_type_id=endpoints[0].data_type_id)

        print("SINGLE SELECT")
        print(item)
        print("END SINGLE SELECT")

        item = await select_by_data_type_id(session=session, data_type_id=-1)

        print("SINGLE SELECT")
        print(item)
        print("END SINGLE SELECT")

    import asyncio
    asyncio.run(main())
