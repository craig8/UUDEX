from datetime import datetime
import pytz
from sqlalchemy import text, Column, TIMESTAMP
from sqlmodel import Field, SQLModel

TZ_UTC = pytz.timezone("UTC")


class BaseModel(SQLModel):

    class Config:
        arbitrary_types_allowed = True


class TimeStampMixin(SQLModel):
    #create_datetime: datetime = Field(default_factory=lambda: datetime.now(TZ_UTC))
    created_datetime: datetime | None = Field(sa_type=TIMESTAMP(timezone=True),
                                              sa_column_kwargs={
                                                  "server_default": text("CURRENT_TIMESTAMP"),
                                              },
                                              nullable=False)
    updated_datetime: datetime | None = Field(sa_type=TIMESTAMP(timezone=True),
                                              sa_column_kwargs={
                                                  "server_default": text("CURRENT_TIMESTAMP"),
                                              },
                                              nullable=False)


class ActiveSwitchMixin():
    active_sw: str = Field(default="Y")


from .authenticated_user import AuthenticatedUser
from .participant_models import Participant, ParticipantCreate, ParticipantDelete
from .endpoint_models import EndPoint
from .dataset_definition_models import DatasetDefinition, DatasetDefinitionCreate, DatasetDefinitionDelete
from .dataset_models import Dataset, DatasetCreate, DatasetDelete
from .attached_data_type_models import AttachedDataType, AttachedDataTypeCreate, AttachedDataTypeDelete
from .data_type_models import DataType, DataTypeCreate, DataTypeDelete
from .subject_models import Subject, SubjectCreate, SubjectDelete
from .subject_policy_models import SubjectPolicy, SubjectPolicyAdd, SubjectPolicyDelete
from .subscription_subject_models import SubscriptionSubject, SubscriptionSubjectAdd, SubscriptionSubjectDelete
from .subscription_models import Subscription, SubscriptionAdd, SubscriptionDelete
