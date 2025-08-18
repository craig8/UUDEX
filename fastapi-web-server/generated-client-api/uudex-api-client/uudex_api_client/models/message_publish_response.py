from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from typing import cast, List
from dateutil.parser import isoparse
from typing import cast
from ..types import UNSET, Unset
import datetime






T = TypeVar("T", bound="MessagePublishResponse")


@_attrs_define
class MessagePublishResponse:
    """ Response model for message publishing.

        Attributes:
            published_count (int): Number of messages successfully published
            subject_uuid (str): UUID of the subject
            message_ids (List[str]): List of message IDs for published messages
            timestamp (Union[Unset, datetime.datetime]): Response timestamp
     """

    published_count: int
    subject_uuid: str
    message_ids: List[str]
    timestamp: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        published_count = self.published_count

        subject_uuid = self.subject_uuid

        message_ids = self.message_ids





        timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "published_count": published_count,
            "subject_uuid": subject_uuid,
            "message_ids": message_ids,
        })
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        published_count = d.pop("published_count")

        subject_uuid = d.pop("subject_uuid")

        message_ids = cast(List[str], d.pop("message_ids"))


        _timestamp = d.pop("timestamp", UNSET)
        timestamp: Union[Unset, datetime.datetime]
        if isinstance(_timestamp,  Unset):
            timestamp = UNSET
        else:
            timestamp = isoparse(_timestamp)




        message_publish_response = cls(
            published_count=published_count,
            subject_uuid=subject_uuid,
            message_ids=message_ids,
            timestamp=timestamp,
        )

        message_publish_response.additional_properties = d
        return message_publish_response

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
