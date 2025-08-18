from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from dateutil.parser import isoparse
from typing import cast
from ..types import UNSET, Unset
import datetime
from typing import Dict
from typing import cast, Union

if TYPE_CHECKING:
  from ..models.subject import Subject
  from ..models.subject_queue_info import SubjectQueueInfo





T = TypeVar("T", bound="SubjectWithMetrics")


@_attrs_define
class SubjectWithMetrics:
    """ Subject with additional metrics and queue information

        Attributes:
            subject (Subject):
            queue_info (SubjectQueueInfo): Information about a subject's message queue
            subscriptions_count (int): Number of subscriptions attached
            last_activity (Union[None, Unset, datetime.datetime]): Last message activity
     """

    subject: 'Subject'
    queue_info: 'SubjectQueueInfo'
    subscriptions_count: int
    last_activity: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.subject import Subject
        from ..models.subject_queue_info import SubjectQueueInfo
        subject = self.subject.to_dict()

        queue_info = self.queue_info.to_dict()

        subscriptions_count = self.subscriptions_count

        last_activity: Union[None, Unset, str]
        if isinstance(self.last_activity, Unset):
            last_activity = UNSET
        elif isinstance(self.last_activity, datetime.datetime):
            last_activity = self.last_activity.isoformat()
        else:
            last_activity = self.last_activity


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "subject": subject,
            "queue_info": queue_info,
            "subscriptions_count": subscriptions_count,
        })
        if last_activity is not UNSET:
            field_dict["last_activity"] = last_activity

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.subject import Subject
        from ..models.subject_queue_info import SubjectQueueInfo
        d = src_dict.copy()
        subject = Subject.from_dict(d.pop("subject"))




        queue_info = SubjectQueueInfo.from_dict(d.pop("queue_info"))




        subscriptions_count = d.pop("subscriptions_count")

        def _parse_last_activity(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_activity_type_0 = isoparse(data)



                return last_activity_type_0
            except: # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_activity = _parse_last_activity(d.pop("last_activity", UNSET))


        subject_with_metrics = cls(
            subject=subject,
            queue_info=queue_info,
            subscriptions_count=subscriptions_count,
            last_activity=last_activity,
        )

        subject_with_metrics.additional_properties = d
        return subject_with_metrics

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
