import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubscriptionAdd")


@_attrs_define
class SubscriptionAdd:
    """
    Attributes:
        subscription_uuid (str):
        subscription_name (str):
        subscription_state (str):
        create_datetime (Union[Unset, datetime.datetime]):
    """

    subscription_uuid: str
    subscription_name: str
    subscription_state: str
    create_datetime: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        subscription_uuid = self.subscription_uuid

        subscription_name = self.subscription_name

        subscription_state = self.subscription_state

        create_datetime: Union[Unset, str] = UNSET
        if not isinstance(self.create_datetime, Unset):
            create_datetime = self.create_datetime.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "subscription_uuid": subscription_uuid,
            "subscription_name": subscription_name,
            "subscription_state": subscription_state,
        })
        if create_datetime is not UNSET:
            field_dict["create_datetime"] = create_datetime

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        subscription_uuid = d.pop("subscription_uuid")

        subscription_name = d.pop("subscription_name")

        subscription_state = d.pop("subscription_state")

        _create_datetime = d.pop("create_datetime", UNSET)
        create_datetime: Union[Unset, datetime.datetime]
        if isinstance(_create_datetime, Unset):
            create_datetime = UNSET
        else:
            create_datetime = isoparse(_create_datetime)

        subscription_add = cls(
            subscription_uuid=subscription_uuid,
            subscription_name=subscription_name,
            subscription_state=subscription_state,
            create_datetime=create_datetime,
        )

        subscription_add.additional_properties = d
        return subscription_add

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
