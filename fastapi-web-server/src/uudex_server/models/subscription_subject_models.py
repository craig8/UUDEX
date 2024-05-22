from datetime import datetime

from sqlmodel import Field, Relationship

from uudex_server.models import BaseModel


class SubscriptionSubjectBase(BaseModel):

    preferred_fulfillment_type: str
    backing_queue_name: str


class SubscriptionSubject(SubscriptionSubjectBase, table=True):
    __tablename__ = 'subscription_subject'

    subscription_subject_id: int | None = Field(default=None, primary_key=True)
    subject_id: int = Field(foreign_key="subject.subject_id", primary_key=True)
    subscription_id: int = Field(foreign_key="subscription.subscription_id", primary_key=True)

    subject: "Subject" = Relationship(back_populates="subscription_links")    # type: ignore
    subscription: "Subscription" = Relationship(back_populates="subject_links")    # type: ignore


class SubscriptionSubjectAdd(SubscriptionSubjectBase):
    pass
