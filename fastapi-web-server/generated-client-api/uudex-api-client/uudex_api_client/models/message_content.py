from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast, Union
from typing import cast
import datetime
from typing import Dict
from typing import Union
from dateutil.parser import isoparse
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.message_content_properties_type_0 import MessageContentPropertiesType0





T = TypeVar("T", bound="MessageContent")


@_attrs_define
class MessageContent:
    """ Individual message from the message broker.

        Attributes:
            payload (str): The message content/payload
            message_id (Union[None, Unset, str]): Unique message identifier
            timestamp (Union[None, Unset, datetime.datetime]): Message timestamp
            properties (Union['MessageContentPropertiesType0', None, Unset]): Additional message properties
     """

    payload: str
    message_id: Union[None, Unset, str] = UNSET
    timestamp: Union[None, Unset, datetime.datetime] = UNSET
    properties: Union['MessageContentPropertiesType0', None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.message_content_properties_type_0 import MessageContentPropertiesType0
        payload = self.payload

        message_id: Union[None, Unset, str]
        if isinstance(self.message_id, Unset):
            message_id = UNSET
        else:
            message_id = self.message_id

        timestamp: Union[None, Unset, str]
        if isinstance(self.timestamp, Unset):
            timestamp = UNSET
        elif isinstance(self.timestamp, datetime.datetime):
            timestamp = self.timestamp.isoformat()
        else:
            timestamp = self.timestamp

        properties: Union[Dict[str, Any], None, Unset]
        if isinstance(self.properties, Unset):
            properties = UNSET
        elif isinstance(self.properties, MessageContentPropertiesType0):
            properties = self.properties.to_dict()
        else:
            properties = self.properties


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "payload": payload,
        })
        if message_id is not UNSET:
            field_dict["message_id"] = message_id
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.message_content_properties_type_0 import MessageContentPropertiesType0
        d = src_dict.copy()
        payload = d.pop("payload")

        def _parse_message_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        message_id = _parse_message_id(d.pop("message_id", UNSET))


        def _parse_timestamp(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                timestamp_type_0 = isoparse(data)



                return timestamp_type_0
            except: # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        timestamp = _parse_timestamp(d.pop("timestamp", UNSET))


        def _parse_properties(data: object) -> Union['MessageContentPropertiesType0', None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                properties_type_0 = MessageContentPropertiesType0.from_dict(data)



                return properties_type_0
            except: # noqa: E722
                pass
            return cast(Union['MessageContentPropertiesType0', None, Unset], data)

        properties = _parse_properties(d.pop("properties", UNSET))


        message_content = cls(
            payload=payload,
            message_id=message_id,
            timestamp=timestamp,
            properties=properties,
        )

        message_content.additional_properties = d
        return message_content

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
