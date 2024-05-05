from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship

from uudex_server.models import BaseDataModel
from uudex_server.models.attached_data_type_models import AttachedDataType


class DataTypeBase(BaseDataModel):
    data_type_uuid: str
    data_type_name: str
    description: str
    schema_definition: str
    specification_reference: str


class DataType(DataTypeBase, table=True):
    __tablename__ = 'data_type'

    data_type_id: Optional[int] = Field(default=None, primary_key=True)
    dataset_definitions: list["DatasetDefinition"] = Relationship(    # type: ignore
        back_populates="data_types", link_model=AttachedDataType)
    # subject_uuid: str = Field(unique=True)
    # subject_short_name: str
    # subject_long_name: str
    # description: str
    # root_org_sw: bool
    # active_sw: bool
    # create_datetime: datetime = Field(default_factory=lambda: datetime.utcnow())


class DataTypeAdd(DataTypeBase):
    pass
