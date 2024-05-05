from datetime import datetime
from typing import Optional

from sqlmodel import Field

from uudex_server.models import BaseDataModel


class SubjectBase(BaseDataModel):
    subject_uuid: str = Field(unique=True)
    subject_name: str
    dataset_instance_key: str
    subscription_type: str
    fulfillment_types_available: str
    full_queue_behavior: str
    max_queue_size_kb: int
    max_message_count: int
    priority: int
    backing_exchange_name: str


class Subject(SubjectBase, table=True):
    subject_id: Optional[int] = Field(default=None, primary_key=True)
    owner_participant_id: int = Field(foreign_key="participant.participant_id", primary_key=True)
    dataset_definition_id: int = Field(foreign_key="dataset_definition.dataset_definition_id",
                                       primary_key=True)


class SubjectAdd(SubjectBase):
    pass
