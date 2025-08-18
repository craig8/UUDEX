from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from ..types import UNSET, Unset
from typing import cast, Union






T = TypeVar("T", bound="SubjectCreate")


@_attrs_define
class SubjectCreate:
    """ Model for creating a new subject

        Attributes:
            subject_name (str):
            dataset_instance_key (str):
            subscription_type (str):
            fulfillment_types_available (str):
            full_queue_behavior (Union[None, str]):
            max_queue_size_kb (Union[None, int]):
            max_message_count (Union[None, int]):
            priority (Union[None, int]):
            backing_exchange_name (str):
            subject_uuid (Union[None, Unset, str]):
            owner_participant_id (Union[None, Unset, int]):
            dataset_definition_id (Union[None, Unset, int]):
     """

    subject_name: str
    dataset_instance_key: str
    subscription_type: str
    fulfillment_types_available: str
    full_queue_behavior: Union[None, str]
    max_queue_size_kb: Union[None, int]
    max_message_count: Union[None, int]
    priority: Union[None, int]
    backing_exchange_name: str
    subject_uuid: Union[None, Unset, str] = UNSET
    owner_participant_id: Union[None, Unset, int] = UNSET
    dataset_definition_id: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        subject_name = self.subject_name

        dataset_instance_key = self.dataset_instance_key

        subscription_type = self.subscription_type

        fulfillment_types_available = self.fulfillment_types_available

        full_queue_behavior: Union[None, str]
        full_queue_behavior = self.full_queue_behavior

        max_queue_size_kb: Union[None, int]
        max_queue_size_kb = self.max_queue_size_kb

        max_message_count: Union[None, int]
        max_message_count = self.max_message_count

        priority: Union[None, int]
        priority = self.priority

        backing_exchange_name = self.backing_exchange_name

        subject_uuid: Union[None, Unset, str]
        if isinstance(self.subject_uuid, Unset):
            subject_uuid = UNSET
        else:
            subject_uuid = self.subject_uuid

        owner_participant_id: Union[None, Unset, int]
        if isinstance(self.owner_participant_id, Unset):
            owner_participant_id = UNSET
        else:
            owner_participant_id = self.owner_participant_id

        dataset_definition_id: Union[None, Unset, int]
        if isinstance(self.dataset_definition_id, Unset):
            dataset_definition_id = UNSET
        else:
            dataset_definition_id = self.dataset_definition_id


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "subject_name": subject_name,
            "dataset_instance_key": dataset_instance_key,
            "subscription_type": subscription_type,
            "fulfillment_types_available": fulfillment_types_available,
            "full_queue_behavior": full_queue_behavior,
            "max_queue_size_kb": max_queue_size_kb,
            "max_message_count": max_message_count,
            "priority": priority,
            "backing_exchange_name": backing_exchange_name,
        })
        if subject_uuid is not UNSET:
            field_dict["subject_uuid"] = subject_uuid
        if owner_participant_id is not UNSET:
            field_dict["owner_participant_id"] = owner_participant_id
        if dataset_definition_id is not UNSET:
            field_dict["dataset_definition_id"] = dataset_definition_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        subject_name = d.pop("subject_name")

        dataset_instance_key = d.pop("dataset_instance_key")

        subscription_type = d.pop("subscription_type")

        fulfillment_types_available = d.pop("fulfillment_types_available")

        def _parse_full_queue_behavior(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        full_queue_behavior = _parse_full_queue_behavior(d.pop("full_queue_behavior"))


        def _parse_max_queue_size_kb(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_queue_size_kb = _parse_max_queue_size_kb(d.pop("max_queue_size_kb"))


        def _parse_max_message_count(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_message_count = _parse_max_message_count(d.pop("max_message_count"))


        def _parse_priority(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        priority = _parse_priority(d.pop("priority"))


        backing_exchange_name = d.pop("backing_exchange_name")

        def _parse_subject_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        subject_uuid = _parse_subject_uuid(d.pop("subject_uuid", UNSET))


        def _parse_owner_participant_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        owner_participant_id = _parse_owner_participant_id(d.pop("owner_participant_id", UNSET))


        def _parse_dataset_definition_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        dataset_definition_id = _parse_dataset_definition_id(d.pop("dataset_definition_id", UNSET))


        subject_create = cls(
            subject_name=subject_name,
            dataset_instance_key=dataset_instance_key,
            subscription_type=subscription_type,
            fulfillment_types_available=fulfillment_types_available,
            full_queue_behavior=full_queue_behavior,
            max_queue_size_kb=max_queue_size_kb,
            max_message_count=max_message_count,
            priority=priority,
            backing_exchange_name=backing_exchange_name,
            subject_uuid=subject_uuid,
            owner_participant_id=owner_participant_id,
            dataset_definition_id=dataset_definition_id,
        )

        subject_create.additional_properties = d
        return subject_create

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
