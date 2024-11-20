from __future__ import annotations
from datetime import datetime
from typing import Optional
from cryptography.hazmat.primitives import serialization

from sqlmodel import Field
import jwt

from uudex_server.models import TimeStampMixin, ActiveSwitchMixin, BaseModel


class EndPointBase(BaseModel):
    endpoint_uuid: str
    endpoint_user_name: str
    certificate_dn: str
    description: str
    uudex_administrator_sw: str
    participant_administrator_sw: str
    participant_id: int


EndpointJwt = str


class EndPoint(EndPointBase, ActiveSwitchMixin, TimeStampMixin, table=True):
    endpoint_id: Optional[int] = Field(default=None, primary_key=True)
    participant_id: int = Field(foreign_key="participant.participant_id")

    # def to_jwt(self, private_key: serialization.PrivateFormat) -> EndpointJwt:

    #     payload = dict(self)
    #     encoded_jwt = jwt.encode(payload=payload, key=private_key, algorithm="HS256")
    #     return encoded_jwt

    # @staticmethod
    # def from_jwt(jwtstr: EndpointJwt) -> EndPoint:

    #     pass


class EndPointCreate(EndPointBase):
    pass


class EndPointDelete(BaseModel):
    endpoint_id: int
