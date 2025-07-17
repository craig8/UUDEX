from __future__ import annotations

from sqlmodel import Field, Relationship

from .participant_models import Participant
from .base import BaseModel, TimeStampMixin, ActiveSwitchMixin
from .common_types import YNSwitch


class EndPointBase(BaseModel):
    endpoint_uuid: str
    endpoint_user_name: str
    certificate_dn: str
    description: str
    uudex_administrator_sw: YNSwitch = Field(max_length=1)    # 'Y' or 'N'
    participant_administrator_sw: YNSwitch = Field(max_length=1)    # 'Y' or 'N'
    participant_id: int


EndpointJwt = str


class EndPoint(EndPointBase, TimeStampMixin, ActiveSwitchMixin, table=True):
    __tablename__ = "endpoint"

    endpoint_id: int | None = Field(default=None, primary_key=True)
    participant_id: int = Field(foreign_key="participant.participant_id")

    # Use a direct string for the relationship
    participant: Participant = Relationship(back_populates="endpoints")


class EndPointCreate(EndPointBase):
    pass


class EndPointDelete(BaseModel):
    endpoint_id: int
