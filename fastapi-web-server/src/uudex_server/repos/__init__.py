from typing import Type, TypeVar, Generic, List, Optional
from sqlmodel import SQLModel, select as _select, delete as _delete, update as _update
from sqlalchemy.ext.asyncio import AsyncSession

# Use BaseModel as the bound for the generic type
from ..models.base import BaseModel

T = TypeVar('T', bound=SQLModel)


class Repository(Generic[T]):

    def __init__(self, model: Type[T], session: AsyncSession, id_field: str | list[str]):
        self._session = session
        self._model = model
        self._id_fields = [id_field] if isinstance(id_field, str) else id_field

    @property
    def model(self) -> Type[T]:
        return self._model

    @property
    def session(self) -> AsyncSession:
        return self._session

    @property
    def id_fields(self) -> list[str]:
        return self._id_fields

    async def select_all(self) -> List[T]:
        statement = _select(self.model)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def select_by_id(self, record_id: int) -> Optional[T]:
        statement = _select(self.model).where(getattr(self.model, self._id_fields[0]) == record_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

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

    async def create(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj


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
