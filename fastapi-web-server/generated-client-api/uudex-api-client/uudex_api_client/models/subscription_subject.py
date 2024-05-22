from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubscriptionSubject")


@_attrs_define
class SubscriptionSubject:
    """
    Attributes:
        preferred_fulfillment_type (str):
        backing_queue_name (str):
        subject_id (int):
        subscription_id (int):
        subscription_subject_id (Union[None, Unset, int]):
    """

    preferred_fulfillment_type: str
    backing_queue_name: str
    subject_id: int
    subscription_id: int
    subscription_subject_id: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        preferred_fulfillment_type = self.preferred_fulfillment_type

        backing_queue_name = self.backing_queue_name

        subject_id = self.subject_id

        subscription_id = self.subscription_id

        subscription_subject_id: Union[None, Unset, int]
        if isinstance(self.subscription_subject_id, Unset):
            subscription_subject_id = UNSET
        else:
            subscription_subject_id = self.subscription_subject_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "preferred_fulfillment_type": preferred_fulfillment_type,
            "backing_queue_name": backing_queue_name,
            "subject_id": subject_id,
            "subscription_id": subscription_id,
        })
        if subscription_subject_id is not UNSET:
            field_dict["subscription_subject_id"] = subscription_subject_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        preferred_fulfillment_type = d.pop("preferred_fulfillment_type")

        backing_queue_name = d.pop("backing_queue_name")

        subject_id = d.pop("subject_id")

        subscription_id = d.pop("subscription_id")

        def _parse_subscription_subject_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        subscription_subject_id = _parse_subscription_subject_id(
            d.pop("subscription_subject_id", UNSET))

        subscription_subject = cls(
            preferred_fulfillment_type=preferred_fulfillment_type,
            backing_queue_name=backing_queue_name,
            subject_id=subject_id,
            subscription_id=subscription_id,
            subscription_subject_id=subscription_subject_id,
        )

        subscription_subject.additional_properties = d
        return subscription_subject

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
