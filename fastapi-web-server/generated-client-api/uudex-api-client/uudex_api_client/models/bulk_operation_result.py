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
  from ..models.bulk_operation_result_failed_item import BulkOperationResultFailedItem





T = TypeVar("T", bound="BulkOperationResult")


@_attrs_define
class BulkOperationResult:
    """ Result of bulk operations

        Attributes:
            successful (List[str]): Successfully processed subject UUIDs
            failed (List['BulkOperationResultFailedItem']): Failed operations with error details
            total_processed (int): Total number of subjects processed
            timestamp (Union[Unset, datetime.datetime]): Operation timestamp
     """

    successful: List[str]
    failed: List['BulkOperationResultFailedItem']
    total_processed: int
    timestamp: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.bulk_operation_result_failed_item import BulkOperationResultFailedItem
        successful = self.successful





        failed = []
        for failed_item_data in self.failed:
            failed_item = failed_item_data.to_dict()
            failed.append(failed_item)





        total_processed = self.total_processed

        timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "successful": successful,
            "failed": failed,
            "total_processed": total_processed,
        })
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.bulk_operation_result_failed_item import BulkOperationResultFailedItem
        d = src_dict.copy()
        successful = cast(List[str], d.pop("successful"))


        failed = []
        _failed = d.pop("failed")
        for failed_item_data in (_failed):
            failed_item = BulkOperationResultFailedItem.from_dict(failed_item_data)



            failed.append(failed_item)


        total_processed = d.pop("total_processed")

        _timestamp = d.pop("timestamp", UNSET)
        timestamp: Union[Unset, datetime.datetime]
        if isinstance(_timestamp,  Unset):
            timestamp = UNSET
        else:
            timestamp = isoparse(_timestamp)




        bulk_operation_result = cls(
            successful=successful,
            failed=failed,
            total_processed=total_processed,
            timestamp=timestamp,
        )

        bulk_operation_result.additional_properties = d
        return bulk_operation_result

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
