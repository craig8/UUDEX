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
from typing import Dict

if TYPE_CHECKING:
  from ..models.message_content import MessageContent





T = TypeVar("T", bound="MessageConsumeResponse")


@_attrs_define
class MessageConsumeResponse:
    """ Response model for message consumption.

        Attributes:
            messages (List['MessageContent']): List of consumed messages
            total_consumed (int): Total number of messages consumed
            subscription_uuid (str): UUID of the subscription
            timestamp (Union[Unset, datetime.datetime]): Response timestamp
     """

    messages: List['MessageContent']
    total_consumed: int
    subscription_uuid: str
    timestamp: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.message_content import MessageContent
        messages = []
        for messages_item_data in self.messages:
            messages_item = messages_item_data.to_dict()
            messages.append(messages_item)





        total_consumed = self.total_consumed

        subscription_uuid = self.subscription_uuid

        timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "messages": messages,
            "total_consumed": total_consumed,
            "subscription_uuid": subscription_uuid,
        })
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.message_content import MessageContent
        d = src_dict.copy()
        messages = []
        _messages = d.pop("messages")
        for messages_item_data in (_messages):
            messages_item = MessageContent.from_dict(messages_item_data)



            messages.append(messages_item)


        total_consumed = d.pop("total_consumed")

        subscription_uuid = d.pop("subscription_uuid")

        _timestamp = d.pop("timestamp", UNSET)
        timestamp: Union[Unset, datetime.datetime]
        if isinstance(_timestamp,  Unset):
            timestamp = UNSET
        else:
            timestamp = isoparse(_timestamp)




        message_consume_response = cls(
            messages=messages,
            total_consumed=total_consumed,
            subscription_uuid=subscription_uuid,
            timestamp=timestamp,
        )

        message_consume_response.additional_properties = d
        return message_consume_response

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
