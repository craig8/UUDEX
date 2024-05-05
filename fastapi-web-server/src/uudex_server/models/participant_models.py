from datetime import datetime
from typing import Optional

from sqlmodel import Field

from uudex_server.models import BaseActiveDataModel


class ParticipantBase(BaseActiveDataModel):
    participant_uuid: str = Field(unique=True)
    participant_short_name: str
    participant_long_name: str
    description: str
    root_org_sw: str


class Participant(ParticipantBase, table=True):
    participant_id: Optional[int] = Field(default=None, primary_key=True)
    # participant_uuid: str = Field(unique=True)
    # participant_short_name: str
    # participant_long_name: str
    # description: str
    # root_org_sw: bool
    # active_sw: bool
    # create_datetime: datetime = Field(default_factory=lambda: datetime.utcnow())


class ParticipantAdd(ParticipantBase):
    pass
