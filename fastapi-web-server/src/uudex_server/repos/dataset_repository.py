from sqlmodel import Session, select
from uudex_server.models import Dataset


def select_all_datasets(session: Session) -> list[Dataset]:
    statement = select(Dataset)
    res = session.exec(statement=statement)
    return list(res)


async def select_dataset_by_id(session: Session, dataset_id: int) -> Dataset | None:
    statement = select(Dataset).where(Dataset.dataset_id == dataset_id)
    res = session.exec(statement=statement)
    return res.first()


if __name__ == '__main__':
    from uudex_server.core.settings import get_settings
    from uudex_server.services.database_service import get_db_session

    settings = get_settings(".env-develop")
    session = get_db_session()
    endpoints = select_all_datasets(session=session)
    for endpoint in endpoints:
        print(endpoint.model_dump_json())

    item = select_dataset_by_id(session=session,
                                dataset_id=endpoints[0].dataset_id)    # type: ignore
    print(item)
