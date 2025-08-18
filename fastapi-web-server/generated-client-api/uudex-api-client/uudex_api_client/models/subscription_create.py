from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SubscriptionCreate")


@_attrs_define
class SubscriptionCreate:
    """ 
        Attributes:
            subscription_uuid (str):
            subscription_name (str):
            subscription_state (str):
            owner_endpoint_id (int):
     """

    subscription_uuid: str
    subscription_name: str
    subscription_state: str
    owner_endpoint_id: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        subscription_uuid = self.subscription_uuid

        subscription_name = self.subscription_name

        subscription_state = self.subscription_state

        owner_endpoint_id = self.owner_endpoint_id


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "subscription_uuid": subscription_uuid,
            "subscription_name": subscription_name,
            "subscription_state": subscription_state,
            "owner_endpoint_id": owner_endpoint_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        subscription_uuid = d.pop("subscription_uuid")

        subscription_name = d.pop("subscription_name")

        subscription_state = d.pop("subscription_state")

        owner_endpoint_id = d.pop("owner_endpoint_id")

        subscription_create = cls(
            subscription_uuid=subscription_uuid,
            subscription_name=subscription_name,
            subscription_state=subscription_state,
            owner_endpoint_id=owner_endpoint_id,
        )

        subscription_create.additional_properties = d
        return subscription_create

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
