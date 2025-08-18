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
  from ..models.queue_management_response_queue_info_type_0 import QueueManagementResponseQueueInfoType0





T = TypeVar("T", bound="QueueManagementResponse")


@_attrs_define
class QueueManagementResponse:
    """ Response model for queue management operations

        Attributes:
            success (bool): Whether the operation succeeded
            message (str): Operation result message
            queue_info (Union['QueueManagementResponseQueueInfoType0', None, Unset]): Queue information if applicable
            timestamp (Union[Unset, datetime.datetime]): Operation timestamp
     """

    success: bool
    message: str
    queue_info: Union['QueueManagementResponseQueueInfoType0', None, Unset] = UNSET
    timestamp: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.queue_management_response_queue_info_type_0 import QueueManagementResponseQueueInfoType0
        success = self.success

        message = self.message

        queue_info: Union[Dict[str, Any], None, Unset]
        if isinstance(self.queue_info, Unset):
            queue_info = UNSET
        elif isinstance(self.queue_info, QueueManagementResponseQueueInfoType0):
            queue_info = self.queue_info.to_dict()
        else:
            queue_info = self.queue_info

        timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "success": success,
            "message": message,
        })
        if queue_info is not UNSET:
            field_dict["queue_info"] = queue_info
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.queue_management_response_queue_info_type_0 import QueueManagementResponseQueueInfoType0
        d = src_dict.copy()
        success = d.pop("success")

        message = d.pop("message")

        def _parse_queue_info(data: object) -> Union['QueueManagementResponseQueueInfoType0', None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                queue_info_type_0 = QueueManagementResponseQueueInfoType0.from_dict(data)



                return queue_info_type_0
            except: # noqa: E722
                pass
            return cast(Union['QueueManagementResponseQueueInfoType0', None, Unset], data)

        queue_info = _parse_queue_info(d.pop("queue_info", UNSET))


        _timestamp = d.pop("timestamp", UNSET)
        timestamp: Union[Unset, datetime.datetime]
        if isinstance(_timestamp,  Unset):
            timestamp = UNSET
        else:
            timestamp = isoparse(_timestamp)




        queue_management_response = cls(
            success=success,
            message=message,
            queue_info=queue_info,
            timestamp=timestamp,
        )

        queue_management_response.additional_properties = d
        return queue_management_response

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
