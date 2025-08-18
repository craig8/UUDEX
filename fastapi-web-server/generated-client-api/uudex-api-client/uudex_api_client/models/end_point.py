import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="EndPoint")


@_attrs_define
class EndPoint:
    """
    Attributes:
        create_datetime (Union[None, datetime.datetime]):
        endpoint_uuid (str):
        endpoint_user_name (str):
        certificate_dn (str):
        description (str):
        uudex_administrator_sw (str):
        participant_administrator_sw (str):
        participant_id (int):
        active_sw (Union[Unset, str]):  Default: 'Y'.
        endpoint_id (Union[None, Unset, int]):
    """

    create_datetime: Union[None, datetime.datetime]
    endpoint_uuid: str
    endpoint_user_name: str
    certificate_dn: str
    description: str
    uudex_administrator_sw: str
    participant_administrator_sw: str
    participant_id: int
    active_sw: Union[Unset, str] = "Y"
    endpoint_id: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        create_datetime: Union[None, str]
        if isinstance(self.create_datetime, datetime.datetime):
            create_datetime = self.create_datetime.isoformat()
        else:
            create_datetime = self.create_datetime

        endpoint_uuid = self.endpoint_uuid

        endpoint_user_name = self.endpoint_user_name

        certificate_dn = self.certificate_dn

        description = self.description

        uudex_administrator_sw = self.uudex_administrator_sw

        participant_administrator_sw = self.participant_administrator_sw

        participant_id = self.participant_id

        active_sw = self.active_sw

        endpoint_id: Union[None, Unset, int]
        if isinstance(self.endpoint_id, Unset):
            endpoint_id = UNSET
        else:
            endpoint_id = self.endpoint_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "create_datetime": create_datetime,
                "endpoint_uuid": endpoint_uuid,
                "endpoint_user_name": endpoint_user_name,
                "certificate_dn": certificate_dn,
                "description": description,
                "uudex_administrator_sw": uudex_administrator_sw,
                "participant_administrator_sw": participant_administrator_sw,
                "participant_id": participant_id,
            }
        )
        if active_sw is not UNSET:
            field_dict["active_sw"] = active_sw
        if endpoint_id is not UNSET:
            field_dict["endpoint_id"] = endpoint_id

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
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        create_datetime = _parse_create_datetime(d.pop("create_datetime"))

        endpoint_uuid = d.pop("endpoint_uuid")

        endpoint_user_name = d.pop("endpoint_user_name")

        certificate_dn = d.pop("certificate_dn")

        description = d.pop("description")

        uudex_administrator_sw = d.pop("uudex_administrator_sw")

        participant_administrator_sw = d.pop("participant_administrator_sw")

        participant_id = d.pop("participant_id")

        active_sw = d.pop("active_sw", UNSET)

        def _parse_endpoint_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        endpoint_id = _parse_endpoint_id(d.pop("endpoint_id", UNSET))

        end_point = cls(
            create_datetime=create_datetime,
            endpoint_uuid=endpoint_uuid,
            endpoint_user_name=endpoint_user_name,
            certificate_dn=certificate_dn,
            description=description,
            uudex_administrator_sw=uudex_administrator_sw,
            participant_administrator_sw=participant_administrator_sw,
            participant_id=participant_id,
            active_sw=active_sw,
            endpoint_id=endpoint_id,
        )

        end_point.additional_properties = d
        return end_point

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
