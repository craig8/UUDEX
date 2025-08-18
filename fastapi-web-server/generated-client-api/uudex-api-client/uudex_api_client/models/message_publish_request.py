from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast, List
from typing import Union






T = TypeVar("T", bound="MessagePublishRequest")


@_attrs_define
class MessagePublishRequest:
    """ Request model for publishing messages to a subject.

        Attributes:
            messages (List[str]): List of message payloads to publish
            payload_encoding (Union[Unset, str]): Encoding type for payloads Default: 'string'.
     """

    messages: List[str]
    payload_encoding: Union[Unset, str] = 'string'
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        messages = self.messages





        payload_encoding = self.payload_encoding


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "messages": messages,
        })
        if payload_encoding is not UNSET:
            field_dict["payload_encoding"] = payload_encoding

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        messages = cast(List[str], d.pop("messages"))


        payload_encoding = d.pop("payload_encoding", UNSET)

        message_publish_request = cls(
            messages=messages,
            payload_encoding=payload_encoding,
        )

        message_publish_request.additional_properties = d
        return message_publish_request

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
