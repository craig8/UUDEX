import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Subscription")


@_attrs_define
class Subscription:
    """
    Attributes:
        subscription_uuid (str):
        subscription_name (str):
        subscription_state (str):
        owner_endpoint_id (int):
        create_datetime (Union[Unset, datetime.datetime]):
        subscription_id (Union[None, Unset, int]):
    """

    subscription_uuid: str
    subscription_name: str
    subscription_state: str
    owner_endpoint_id: int
    create_datetime: Union[Unset, datetime.datetime] = UNSET
    subscription_id: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        subscription_uuid = self.subscription_uuid

        subscription_name = self.subscription_name

        subscription_state = self.subscription_state

        owner_endpoint_id = self.owner_endpoint_id

        create_datetime: Union[Unset, str] = UNSET
        if not isinstance(self.create_datetime, Unset):
            create_datetime = self.create_datetime.isoformat()

        subscription_id: Union[None, Unset, int]
        if isinstance(self.subscription_id, Unset):
            subscription_id = UNSET
        else:
            subscription_id = self.subscription_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "subscription_uuid": subscription_uuid,
            "subscription_name": subscription_name,
            "subscription_state": subscription_state,
            "owner_endpoint_id": owner_endpoint_id,
        })
        if create_datetime is not UNSET:
            field_dict["create_datetime"] = create_datetime
        if subscription_id is not UNSET:
            field_dict["subscription_id"] = subscription_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        subscription_uuid = d.pop("subscription_uuid")

        subscription_name = d.pop("subscription_name")

        subscription_state = d.pop("subscription_state")

        owner_endpoint_id = d.pop("owner_endpoint_id")

        _create_datetime = d.pop("create_datetime", UNSET)
        create_datetime: Union[Unset, datetime.datetime]
        if isinstance(_create_datetime, Unset):
            create_datetime = UNSET
        else:
            create_datetime = isoparse(_create_datetime)

        def _parse_subscription_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        subscription_id = _parse_subscription_id(d.pop("subscription_id", UNSET))

        subscription = cls(
            subscription_uuid=subscription_uuid,
            subscription_name=subscription_name,
            subscription_state=subscription_state,
            owner_endpoint_id=owner_endpoint_id,
            create_datetime=create_datetime,
            subscription_id=subscription_id,
        )

        subscription.additional_properties = d
        return subscription

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
