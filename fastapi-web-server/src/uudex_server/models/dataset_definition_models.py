from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship

from uudex_server.models import BaseDataModel
from uudex_server.models.attached_data_type_models import AttachedDataType


class DatasetDefinitionBase(BaseDataModel):
    dataset_definition_uuid: str
    dataset_definition_name: str
    description: str


class DatasetDefinition(DatasetDefinitionBase, table=True):
    __tablename__ = 'dataset_definition'

    dataset_definition_id: Optional[int] = Field(default=None, primary_key=True)
    data_types: list["DataType"] = Relationship(    # type: ignore
        back_populates="dataset_definitions", link_model=AttachedDataType)


class DatasetDefinitionAdd(DatasetDefinitionBase):
    pass
