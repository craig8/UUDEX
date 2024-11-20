from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship

from uudex_server.models import TimeStampMixin, BaseModel, ActiveSwitchMixin


class ParticipantBase(BaseModel):
    participant_uuid: str = Field(unique=True)
    participant_short_name: str
    participant_long_name: str
    description: str
    root_org_sw: str = Field(default="Y")


class Participant(ParticipantBase, TimeStampMixin, ActiveSwitchMixin, table=True):
    participant_id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship to datasets
    datasets: list["Dataset"] = Relationship(back_populates="owner")


class ParticipantCreate(ParticipantBase):
    pass


class ParticipantDelete(BaseModel):
    participant_id: int
