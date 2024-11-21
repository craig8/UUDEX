from typing import Type, TypeVar, Generic, List, Optional
from sqlmodel import Session, SQLModel, select as _select, delete as _delete, update as _update

# Use BaseModel as the bound for the generic type
from uudex_server.models import BaseModel

T = TypeVar('T', bound=BaseModel)


class Repository(Generic[T]):

    def __init__(self, model: Type[T], id_field: str | list[str]):
        self._model = model
        if isinstance(id_field, str):
            self._id_fields = [id_field]
        else:
            self._id_fields = id_field

    @property
    def model(self) -> Type[T]:
        return self._model

    @property
    def id_fields(self) -> list[str]:
        return self._id_fields

    async def select_all(self, session: Session) -> List[T]:
        statement = _select(self.model)
        res = session.exec(statement)
        return list(res)

    async def select_by_id(self, session: Session, record_id: int) -> Optional[T]:
        if len(self._id_fields) > 1:
            raise ValueError("Multiple ids required as key value pairs for this repository")

        statement = _select(self.model).where(getattr(self.model, self._id_fields[0]) == record_id)
        res = session.exec(statement)
        return res.first()

    async def select_by_ids(self, session: Session, **ids: int) -> Optional[T]:
        statements = [getattr(self.model, field) == ids[field] for field in self.id_fields]
        statement = _select(self.model).where(*statements)
        res = session.exec(statement)
        return res.first()

    async def select_by_fields(self, session: Session, **ids: int) -> Optional[T]:
        statements = [
            getattr(self.model, field) == ids[field] for field in self.model.model_fields
            if field in ids
        ]
        statement = _select(self.model).where(*statements)
        res = session.exec(statement)
        return res.first()

    async def delete(self, session: Session, obj: BaseModel) -> None:
        statements = [
            getattr(self.model, field) == getattr(obj, field) for field in self.id_fields
        ]
        statement = _delete(self.model).where(*statements)
        session.exec(statement)
        session.commit()

    async def update(self, session: Session, obj: T) -> T:
        statements = [
            getattr(self.model, field) == getattr(obj, field) for field in self.id_fields
        ]
        statement = _update(
            self.model).where(*statements).values(**obj.model_dump(exclude_unset=True))
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
from .attached_data_type_repository import AttachedDataTypeRepository
from .data_type_repository import DataTypeRepository
from .dataset_definition_repository import DatasetDefinitionRepository
from .subject_repository import SubjectRepository
from .dataset_repository import DatasetRepository
from .endpoint_repository import EndpointRepository
from .subject_policy_repository import SubjectPolicyRepository
from .subscription_repository import SubscriptionRepository
from .subject_repository import SubjectRepository
from .subscription_subject_repository import SubscriptionSubjectRepository
from .participant_repository import ParticipantRepository
