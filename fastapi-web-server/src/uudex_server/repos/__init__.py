from typing import Type, TypeVar, Generic, List, Optional
from sqlmodel import Session, SQLModel, select as _select, delete as _delete, update as _update

# Use BaseModel as the bound for the generic type
from uudex_server.models import BaseModel

T = TypeVar('T', bound=BaseModel)


class Repository(Generic[T]):

    def __init__(self, model: Type[T], id_field: str):
        self._model = model
        self._id_field = id_field

    @property
    def model(self) -> Type[T]:
        return self._model

    @property
    def id_field(self) -> str:
        return self._id_field

    async def select_all(self, session: Session) -> List[T]:
        statement = _select(self.model)
        res = session.exec(statement)
        return list(res)

    async def select_by_id(self, session: Session, record_id: int) -> Optional[T]:
        statement = _select(self.model).where(getattr(self.model, self.id_field) == record_id)
        res = session.exec(statement)
        return res.first()

    async def delete(self, session: Session, obj: BaseModel) -> None:
        statement = _delete(
            self.model).where(getattr(self.model, self.id_field) == getattr(obj, self.id_field))
        session.exec(statement)
        session.commit()

    async def update(self, session: Session, obj: T) -> T:
        statement = _update(self.model).where(
            getattr(self.model, self.id_field) == getattr(obj, self.id_field)).values(
                **obj.model_dump(exclude_unset=True))
        session.exec(statement)
        session.commit()
        session.refresh(obj)
        return obj

    async def create(self, session: Session, obj: BaseModel) -> T:
        db_obj = self.model(**obj.model_dump())
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj


# Importing repository modules with standardized function names
from .data_type_repository import DataTypeRepository
# from .dataset_definition_repository import Dat
# from . import attached_data_type_repository as AttachedDataTypeRepo
# # from . import data_type_repository as DataTypeRepo
#
# from . import dataset_definition_repository as DatasetDefinitionRepo
# from . import dataset_repository as DatasetRepo
# from . import endpoint_repository as EndpointRepo
# from . import participant_repository as ParticipantRepo
# from . import subject_repository as SubjectRepo
# from . import subscription_repository as SubscriptionRepo
