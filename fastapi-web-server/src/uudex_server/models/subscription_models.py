from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship

from uudex_server.models import BaseDataModel
from uudex_server.models.subscription_subject_models import SubscriptionSubject


class SubscriptionBase(BaseDataModel):

    subscription_uuid: str
    subscription_name: str
    subscription_state: str


class Subscription(SubscriptionBase, table=True):
    subscription_id: Optional[int] = Field(default=None, primary_key=True)
    owner_endpoint_id: int = Field(foreign_key="endpoint.owner_endpoint_id")

    subject_links: list[SubscriptionSubject] = Relationship(
        back_populates="subscription")    # type: ignore


class SubscriptionAdd(SubscriptionBase):
    pass
