from uudex_server.models import Dataset
from sqlmodel import Session, select as _select
import uudex_server.models as m
from uudex_server.repos import Repository


class DatasetRepository(Repository[Dataset]):

    def __init__(self, session: Session):
        super().__init__(m.Dataset, session=session, id_field="dataset_id")

    async def select_datasets_by_participant(self, session: Session,
                                             participant_id: int) -> list[m.Dataset]:
        statement = _select(m.Dataset).where(Dataset.owner_participant_id == participant_id)
        res = session.exec(statement)
        return list(res)


class DatasetDefinitionRepository(Repository[m.DatasetDefinition]):

    def __init__(self, session: Session):
        super().__init__(m.DatasetDefinition, session=session, id_field="dataset_definition_id")
