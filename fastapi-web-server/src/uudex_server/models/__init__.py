from datetime import datetime
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):

    class Config:
        arbitrary_types_allowed = True


class BaseDataModel(BaseModel):
    create_datetime: datetime = Field(default_factory=lambda: datetime.utcnow())


class BaseActiveDataModel(BaseDataModel):
    active_sw: str


from .participant_models import Participant, ParticipantAdd
from .endpoint_models import EndPoint
from .subject_models import Subject, SubjectAdd
from .dataset_definition_models import DatasetDefinition, DatasetDefinitionAdd
from .dataset_models import Dataset, DatasetAdd
from .attached_data_type_models import AttachedDataType, AttachedDataTypeAdd
from .data_type_models import DataType, DataTypeAdd
from .subject_policy_models import SubjectPolicy, SubjectPolicyAdd
from .subscription_subject_models import SubscriptionSubject, SubscriptionSubjectAdd
from .subscription_models import Subscription, SubscriptionAdd
