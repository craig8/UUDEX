from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship

from .base import BaseModel, TimeStampMixin

from uudex_server.models.subscription_subject_models import SubscriptionSubject


class SubjectBase(BaseModel):
    subject_uuid: str = Field(unique=True)
    subject_name: str
    dataset_instance_key: str
    subscription_type: str
    fulfillment_types_available: str
    full_queue_behavior: str | None
    max_queue_size_kb: int | None
    max_message_count: int | None
    priority: int | None
    backing_exchange_name: str
    owner_participant_id: int
    dataset_definition_id: int


class Subject(SubjectBase, TimeStampMixin, table=True):
    subject_id: int | None = Field(default=None, primary_key=True)
    owner_participant_id: int = Field(foreign_key="participant.participant_id", index=True)
    dataset_definition_id: int = Field(foreign_key="dataset_definition.dataset_definition_id",
                                       index=True)

    subscription_links: list[SubscriptionSubject] = Relationship(
        back_populates="subject")    # type: ignore

    # Relationship to datasets
    datasets: list["Dataset"] = Relationship(back_populates="subject")    # type: ignore


class SubjectCreate(SubjectBase):
    pass


class SubjectDelete(BaseModel):
    subject_id: int
