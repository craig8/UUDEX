from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship

from .base import BaseModel, TimeStampMixin, ActiveSwitchMixin


class ParticipantBase(BaseModel):
    participant_uuid: str    # UUID stored as a string
    participant_short_name: str
    participant_long_name: str
    description: Optional[str] = None
    root_org_sw: str


class Participant(ParticipantBase, TimeStampMixin, ActiveSwitchMixin, table=True):
    __tablename__ = "participant"

    participant_id: int | None = Field(default=None, primary_key=True)

    contacts: list["Contact"] = Relationship(back_populates="participant")
    endpoints: list["EndPoint"] = Relationship(back_populates="participant")
    datasets: list["Dataset"] = Relationship(back_populates="owner")

    # # Align relationships with descriptive names
    # participant_visibility_exposed_by: list["ParticipantVisibility"] = Relationship(
    #     back_populates="exposed_by_participant"
    # )
    # participant_visibility_exposed_to: list["ParticipantVisibility"] = Relationship(
    #     back_populates="exposed_to_participant"
    # )


class ParticipantCreate(ParticipantBase):
    pass


class ParticipantDelete(BaseModel):
    participant_id: int
