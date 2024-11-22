import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field

from .base import TimeStampMixin, BaseModel


class DatasetBase(BaseModel):
    dataset_uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), nullable=False)
    dataset_name: str
    description: str
    properties: str
    payload: bytes
    payload_size: int
    payload_md5_hash: str
    payload_compression_algorithm: str
    version_number: int


# class Dataset(DatasetBase, TimeStampMixin, table=True):
#     __tablename__ = "dataset"
#
#     dataset_id: Optional[int] = Field(default=None, primary_key=True)
#     owner_participant_id: int = Field(foreign_key="participant.participant_id", primary_key=True)
#     subject_id: int = Field(foreign_key="subject.subject_id", primary_key=True)
#
#
class DatasetCreate(DatasetBase):
    owner_participant_id: int
    subject_id: int


class DatasetDelete(BaseModel):
    dataset_id: int


from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
import uuid


class Dataset(SQLModel, table=True):
    dataset_id: Optional[int] = Field(default=None, primary_key=True)
    dataset_uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), nullable=False)
    dataset_name: str
    description: str
    properties: str
    payload: bytes
    payload_size: int
    payload_md5_hash: str
    payload_compression_algorithm: str
    version_number: int
    owner_participant_id: int = Field(foreign_key="participant.participant_id")
    subject_id: int = Field(foreign_key="subject.subject_id")

    owner: Optional["Participant"] = Relationship(back_populates="datasets")
    subject: Optional["Subject"] = Relationship(back_populates="datasets")
