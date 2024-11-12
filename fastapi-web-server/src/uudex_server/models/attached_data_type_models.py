from datetime import datetime
from typing import Optional

from sqlmodel import Field

from uudex_server.models import TimeStampMixin, BaseModel


class AttachedDataTypeBase(BaseModel):
    pass


class AttachedDataType(AttachedDataTypeBase, table=True):
    __tablename__ = 'attached_data_type'

    dataset_definition_id: int = Field(foreign_key="dataset_definition.dataset_definition_id",
                                       primary_key=True)

    data_type_id: int = Field(foreign_key="data_type.data_type_id", primary_key=True)


class AttachedDataTypeCreate(AttachedDataType):
    pass
    # dataset_definition_id: int
    # data_type_id: int


class AttachedDataTypeRemove(AttachedDataType):
    pass
    # dataset_definition_id: int
    # data_type_id = int
