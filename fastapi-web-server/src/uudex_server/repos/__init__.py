from typing import Type, TypeVar, Generic, List, Optional
from sqlmodel import Session, SQLModel, select as _select, delete as _delete, update as _update

# Use BaseModel as the bound for the generic type
from ..models.base import BaseModel

T = TypeVar('T', bound=BaseModel)


class Repository(Generic[T]):

    def __init__(self, model: Type[T], session: Session, id_field: str | list[str]):
        self._session = session
        self._model = model
        if isinstance(id_field, str):
            self._id_fields = [id_field]
        else:
            self._id_fields = id_field

    @property
    def session(self) -> Session:
        return self._session

    @property
    def model(self) -> Type[T]:
        return self._model

    @property
    def id_fields(self) -> list[str]:
        return self._id_fields

    async def select_all(self) -> List[T]:
        statement = _select(self.model)
        res = self.session.exec(statement)
        return list(res)

    async def select_by_id(self, record_id: int) -> Optional[T]:
        if len(self._id_fields) > 1:
            raise ValueError("Multiple ids required as key value pairs for this repository")

        statement = _select(self.model).where(getattr(self.model, self._id_fields[0]) == record_id)
        res = self.session.exec(statement)
        return res.first()

    async def select_by_ids(self, **ids: int) -> Optional[T]:
        statements = [getattr(self.model, field) == ids[field] for field in self.id_fields]
        statement = _select(self.model).where(*statements)
        res = self.session.exec(statement)
        return res.first()

    async def select_by_fields(self, **ids: int) -> Optional[T]:
        statements = [
            getattr(self.model, field) == ids[field] for field in self.model.model_fields
            if field in ids
        ]
        statement = _select(self.model).where(*statements)
        res = self.session.exec(statement)
        return res.first()

    async def delete(self, obj: BaseModel) -> None:
        statements = [
            getattr(self.model, field) == getattr(obj, field) for field in self.id_fields
        ]
        statement = _delete(self.model).where(*statements)
        self.session.exec(statement)
        self.session.commit()

    async def update(self, obj: T) -> T:
        statements = [
            getattr(self.model, field) == getattr(obj, field) for field in self.id_fields
        ]
        statement = _update(
            self.model).where(*statements).values(**obj.model_dump(exclude_unset=True))
        self.session.exec(statement)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    async def create(self, obj: BaseModel) -> T:
        db_obj = self.model(**obj.model_dump())
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj


# Importing repository modules with standardized function names
from .attached_data_type_repository import AttachedDataTypeRepository
from .data_type_repository import DataTypeRepository
from .dataset_definition_repository import DatasetDefinitionRepository
from .subscription_and_subject_repositories import SubjectRepository
from .dataset_repositories import DatasetRepository
from .endpoint_repository import EndpointRepository
from .subject_policy_repositories import (SubjectPolicyAclConstraintRepository,
                                          SubjectPolicyRepository, GrantScopeRepository,
                                          SubjectAclRepository, SubjectAclGrantRepository,
                                          SubjectPolicyGrantAllowedRepository)
from .subscription_and_subject_repositories import SubscriptionSubjectRepository, SubscriptionRepository
from .participant_repositories import ParticipantRepository, ParticipantVisibilityRepository
