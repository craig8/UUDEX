from datetime import datetime
from typing import Optional

from sqlmodel import Field

from uudex_server.models import BaseDataModel


class SubscriptionBase(BaseDataModel):

    subscription_uuid: str
    subscription_name: str
    subscription_state: str


class Subscription(SubscriptionBase, table=True):
    subscription_subject_id: Optional[int] = Field(default=None, primary_key=True)
    owner_endpoint_id: int = Field(foreign_key="endpoint.owner_endpoint_id")


class SubscriptionAdd(SubscriptionBase):
    pass
