from datetime import datetime
from typing import Optional

from sqlmodel import Field

from uudex_server.models import BaseDataModel


class SubscriptionSubjectBase(BaseDataModel):

    preferred_fulfillment_type: str
    backing_queue_name: str


class SubscriptionSubject(SubscriptionSubjectBase, table=True):
    __tablename__ = 'subscription_subject'

    subscription_subject_id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: int = Field(foreign_key="subject.subject_id", primary_key=True)
    subscription_id: int = Field(foreign_key="subscription.subscription_id", primary_key=True)


class SubscriptionSubjectAdd(SubscriptionSubjectBase):
    pass
