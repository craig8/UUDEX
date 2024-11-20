from uudex_server.models import Dataset
from typing import Awaitable
from sqlmodel import Session, select as _select, delete as _delete
from uudex_server.models import DatasetDefinition, DatasetDefinitionCreate, DatasetDefinitionDelete

from uudex_server.models.dataset_models import Dataset
from uudex_server.repos import Repository


class DatasetRepository(Repository[Dataset]):

    def __init__(self):
        super().__init__(Dataset, id_field="dataset_id")

    async def select_datasets_by_participant(self, session: Session,
                                             participant_id: int) -> list[Dataset]:
        statement = _select(Dataset).where(Dataset.owner_participant_id == participant_id)
        res = session.exec(statement)
        return list(res)


# def select_all_datasets(session: Session) -> list[Dataset]:
#     statement = _select(Dataset)
#     res = session.exec(statement=statement)
#     return list(res)
#
#
# async def select_dataset_by_id(session: Session, dataset_id: int) -> Dataset | None:
#     statement = _select(Dataset).where(Dataset.dataset_id == dataset_id)
#     res = session.exec(statement=statement)
#     return res.first()
#
#
# async def select_by_data_definition_id(
#         session: Session, data_definition_id: int) -> Awaitable[DatasetDefinition] | None:
#     statement = _select(DatasetDefinition).where(
#         DatasetDefinition.dataset_definition_id == data_definition_id)
#     res = session.exec(statement=statement)
#     return res.first()    # type: ignore
#
# async def create(session: Session, dataset_definition: DatasetDefinitionCreate) -> DatasetDefinition:
#     ds_def = DatasetDefinition(**dataset_definition.dict())
#     session.add(ds_def)
#     session.commit()
#     session.refresh(ds_def)
#     return ds_def
#
# async def select_all(session: Session) -> list[DatasetDefinition]:
#     statement = _select(DatasetDefinition)
#     res = session.exec(statement)
#     return list(res)
#
# async def select_by_id(session: Session, dataset_definition_id: int) -> DatasetDefinition | None:
#     statement = _select(DatasetDefinition).where(DatasetDefinition.dataset_definition_id == dataset_definition_id)
#     res = session.exec(statement)
#     return res.first()
#
# async def update(session: Session, dataset_definition: DatasetDefinition) -> DatasetDefinition:
#     session.add(dataset_definition)
#     session.commit()
#     session.refresh(dataset_definition)
#     return dataset_definition
#
# async def delete(session: Session, dataset_definition_remove: DatasetDefinitionDelete) -> None:
#     statement = _delete(DatasetDefinition).where(DatasetDefinition.dataset_definition_id == dataset_definition_remove.dataset_definition_id)
#     session.exec(statement)
#     session.commit()
#
# if __name__ == '__main__':
#
#     async def main():
#         from uudex_server.core.settings import get_settings
#         from uudex_server.services.database_service import get_db_session
#
#         settings = get_settings(".env-develop")
#         session = get_db_session()
#         endpoints = select_all(session=session)
#         print("LIST")
#         for endpoint in endpoints:
#             print(endpoint.model_dump_json())
#         print("END LIST")
#
#         item = await select_by_data_definition_id(session=session, data_definition_id=endpoints[0].dataset_definition_id)
#
#         print("SINGLE SELECT")
#         print(item)
#         print("END SINGLE SELECT")
#
#     import asyncio
#     asyncio.run(main())
#
# if __name__ == '__main__':
#     from uudex_server.core.settings import get_settings
#     from uudex_server.services.database_service import get_db_session
#
#     settings = get_settings(".env-develop")
#     session = get_db_session()
#     endpoints = select_all_datasets(session=session)
#     for endpoint in endpoints:
#         print(endpoint.model_dump_json())
#
#     item = select_dataset_by_id(session=session,
#                                 dataset_id=endpoints[0].dataset_id)    # type: ignore
#     print(item)
