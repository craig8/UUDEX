from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast, Union
from typing import Union






T = TypeVar("T", bound="SubjectUpdate")


@_attrs_define
class SubjectUpdate:
    """ Model for updating an existing subject

        Attributes:
            subject_name (Union[None, Unset, str]):
            dataset_instance_key (Union[None, Unset, str]):
            subscription_type (Union[None, Unset, str]):
            fulfillment_types_available (Union[None, Unset, str]):
            full_queue_behavior (Union[None, Unset, str]):
            max_queue_size_kb (Union[None, Unset, int]):
            max_message_count (Union[None, Unset, int]):
            priority (Union[None, Unset, int]):
            backing_exchange_name (Union[None, Unset, str]):
     """

    subject_name: Union[None, Unset, str] = UNSET
    dataset_instance_key: Union[None, Unset, str] = UNSET
    subscription_type: Union[None, Unset, str] = UNSET
    fulfillment_types_available: Union[None, Unset, str] = UNSET
    full_queue_behavior: Union[None, Unset, str] = UNSET
    max_queue_size_kb: Union[None, Unset, int] = UNSET
    max_message_count: Union[None, Unset, int] = UNSET
    priority: Union[None, Unset, int] = UNSET
    backing_exchange_name: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        subject_name: Union[None, Unset, str]
        if isinstance(self.subject_name, Unset):
            subject_name = UNSET
        else:
            subject_name = self.subject_name

        dataset_instance_key: Union[None, Unset, str]
        if isinstance(self.dataset_instance_key, Unset):
            dataset_instance_key = UNSET
        else:
            dataset_instance_key = self.dataset_instance_key

        subscription_type: Union[None, Unset, str]
        if isinstance(self.subscription_type, Unset):
            subscription_type = UNSET
        else:
            subscription_type = self.subscription_type

        fulfillment_types_available: Union[None, Unset, str]
        if isinstance(self.fulfillment_types_available, Unset):
            fulfillment_types_available = UNSET
        else:
            fulfillment_types_available = self.fulfillment_types_available

        full_queue_behavior: Union[None, Unset, str]
        if isinstance(self.full_queue_behavior, Unset):
            full_queue_behavior = UNSET
        else:
            full_queue_behavior = self.full_queue_behavior

        max_queue_size_kb: Union[None, Unset, int]
        if isinstance(self.max_queue_size_kb, Unset):
            max_queue_size_kb = UNSET
        else:
            max_queue_size_kb = self.max_queue_size_kb

        max_message_count: Union[None, Unset, int]
        if isinstance(self.max_message_count, Unset):
            max_message_count = UNSET
        else:
            max_message_count = self.max_message_count

        priority: Union[None, Unset, int]
        if isinstance(self.priority, Unset):
            priority = UNSET
        else:
            priority = self.priority

        backing_exchange_name: Union[None, Unset, str]
        if isinstance(self.backing_exchange_name, Unset):
            backing_exchange_name = UNSET
        else:
            backing_exchange_name = self.backing_exchange_name


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if subject_name is not UNSET:
            field_dict["subject_name"] = subject_name
        if dataset_instance_key is not UNSET:
            field_dict["dataset_instance_key"] = dataset_instance_key
        if subscription_type is not UNSET:
            field_dict["subscription_type"] = subscription_type
        if fulfillment_types_available is not UNSET:
            field_dict["fulfillment_types_available"] = fulfillment_types_available
        if full_queue_behavior is not UNSET:
            field_dict["full_queue_behavior"] = full_queue_behavior
        if max_queue_size_kb is not UNSET:
            field_dict["max_queue_size_kb"] = max_queue_size_kb
        if max_message_count is not UNSET:
            field_dict["max_message_count"] = max_message_count
        if priority is not UNSET:
            field_dict["priority"] = priority
        if backing_exchange_name is not UNSET:
            field_dict["backing_exchange_name"] = backing_exchange_name

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        def _parse_subject_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        subject_name = _parse_subject_name(d.pop("subject_name", UNSET))


        def _parse_dataset_instance_key(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dataset_instance_key = _parse_dataset_instance_key(d.pop("dataset_instance_key", UNSET))


        def _parse_subscription_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        subscription_type = _parse_subscription_type(d.pop("subscription_type", UNSET))


        def _parse_fulfillment_types_available(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        fulfillment_types_available = _parse_fulfillment_types_available(d.pop("fulfillment_types_available", UNSET))


        def _parse_full_queue_behavior(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        full_queue_behavior = _parse_full_queue_behavior(d.pop("full_queue_behavior", UNSET))


        def _parse_max_queue_size_kb(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_queue_size_kb = _parse_max_queue_size_kb(d.pop("max_queue_size_kb", UNSET))


        def _parse_max_message_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_message_count = _parse_max_message_count(d.pop("max_message_count", UNSET))


        def _parse_priority(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        priority = _parse_priority(d.pop("priority", UNSET))


        def _parse_backing_exchange_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        backing_exchange_name = _parse_backing_exchange_name(d.pop("backing_exchange_name", UNSET))


        subject_update = cls(
            subject_name=subject_name,
            dataset_instance_key=dataset_instance_key,
            subscription_type=subscription_type,
            fulfillment_types_available=fulfillment_types_available,
            full_queue_behavior=full_queue_behavior,
            max_queue_size_kb=max_queue_size_kb,
            max_message_count=max_message_count,
            priority=priority,
            backing_exchange_name=backing_exchange_name,
        )

        subject_update.additional_properties = d
        return subject_update

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
