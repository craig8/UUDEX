from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SubjectQueueInfo")


@_attrs_define
class SubjectQueueInfo:
    """ Information about a subject's message queue

        Attributes:
            subject_uuid (str): Subject UUID
            subject_name (str): Subject name
            exchange_name (str): Message broker exchange name
            queue_count (int): Number of queues associated with this subject
            total_messages (int): Total messages across all queues
            total_consumers (int): Total consumers across all queues
     """

    subject_uuid: str
    subject_name: str
    exchange_name: str
    queue_count: int
    total_messages: int
    total_consumers: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        subject_uuid = self.subject_uuid

        subject_name = self.subject_name

        exchange_name = self.exchange_name

        queue_count = self.queue_count

        total_messages = self.total_messages

        total_consumers = self.total_consumers


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "subject_uuid": subject_uuid,
            "subject_name": subject_name,
            "exchange_name": exchange_name,
            "queue_count": queue_count,
            "total_messages": total_messages,
            "total_consumers": total_consumers,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        subject_uuid = d.pop("subject_uuid")

        subject_name = d.pop("subject_name")

        exchange_name = d.pop("exchange_name")

        queue_count = d.pop("queue_count")

        total_messages = d.pop("total_messages")

        total_consumers = d.pop("total_consumers")

        subject_queue_info = cls(
            subject_uuid=subject_uuid,
            subject_name=subject_name,
            exchange_name=exchange_name,
            queue_count=queue_count,
            total_messages=total_messages,
            total_consumers=total_consumers,
        )

        subject_queue_info.additional_properties = d
        return subject_queue_info

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
