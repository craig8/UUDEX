from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlmodel import Field

from uudex_server.models import BaseActiveDataModel, BaseModel


class EndPointBase(BaseActiveDataModel):
    endpoint_uuid: str
    endpoint_user_name: str
    certificate_dn: str
    description: str
    uudex_administrator_sw: str
    participant_administrator_sw: str


class EndPoint(EndPointBase, table=True):
    endpoint_id: Optional[int] = Field(default=None, primary_key=True)
    participant_id: int = Field(foreign_key="participant.participant_id")

