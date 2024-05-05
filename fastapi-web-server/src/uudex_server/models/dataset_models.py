from datetime import datetime
from typing import Optional

from sqlmodel import Field

from uudex_server.models import BaseDataModel


class DatasetBase(BaseDataModel):
    dataset_uuid: str = Field(unique=True)
    dataset_name: str
    description: str
    properties: str
    payload: bytes
    payload_size: int
    payload_md5_hash: str
    payload_compression_algorithm: str
    version_number: int


class Dataset(DatasetBase, table=True):

    dataset_id: Optional[int] = Field(default=None, primary_key=True)
    owner_participant_id: int = Field(foreign_key="participant.participant_id", primary_key=True)
    subject_id: int = Field(foreign_key="subject.subject_id", primary_key=True)


class DatasetAdd(DatasetBase):
    pass
