from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast, Union
from typing import cast
import datetime
from typing import Union
from dateutil.parser import isoparse
from ..types import UNSET, Unset






T = TypeVar("T", bound="Subscription")


@_attrs_define
class Subscription:
    """ 
        Attributes:
            create_datetime (Union[None, datetime.datetime]):
            subscription_uuid (str):
            subscription_name (str):
            subscription_state (str):
            owner_endpoint_id (int):
            subscription_id (Union[None, Unset, int]):
     """

    create_datetime: Union[None, datetime.datetime]
    subscription_uuid: str
    subscription_name: str
    subscription_state: str
    owner_endpoint_id: int
    subscription_id: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        create_datetime: Union[None, str]
        if isinstance(self.create_datetime, datetime.datetime):
            create_datetime = self.create_datetime.isoformat()
        else:
            create_datetime = self.create_datetime

        subscription_uuid = self.subscription_uuid

        subscription_name = self.subscription_name

        subscription_state = self.subscription_state

        owner_endpoint_id = self.owner_endpoint_id

        subscription_id: Union[None, Unset, int]
        if isinstance(self.subscription_id, Unset):
            subscription_id = UNSET
        else:
            subscription_id = self.subscription_id


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "create_datetime": create_datetime,
            "subscription_uuid": subscription_uuid,
            "subscription_name": subscription_name,
            "subscription_state": subscription_state,
            "owner_endpoint_id": owner_endpoint_id,
        })
        if subscription_id is not UNSET:
            field_dict["subscription_id"] = subscription_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        def _parse_create_datetime(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                create_datetime_type_0 = isoparse(data)



                return create_datetime_type_0
            except: # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        create_datetime = _parse_create_datetime(d.pop("create_datetime"))


        subscription_uuid = d.pop("subscription_uuid")

        subscription_name = d.pop("subscription_name")

        subscription_state = d.pop("subscription_state")

        owner_endpoint_id = d.pop("owner_endpoint_id")

        def _parse_subscription_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        subscription_id = _parse_subscription_id(d.pop("subscription_id", UNSET))


        subscription = cls(
            create_datetime=create_datetime,
            subscription_uuid=subscription_uuid,
            subscription_name=subscription_name,
            subscription_state=subscription_state,
            owner_endpoint_id=owner_endpoint_id,
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
