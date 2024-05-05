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
        active_sw (str):
        endpoint_uuid (str):
        endpoint_user_name (str):
        certificate_dn (str):
        description (str):
        uudex_administrator_sw (str):
        participant_administrator_sw (str):
        participant_id (int):
        create_datetime (Union[Unset, datetime.datetime]):
        endpoint_id (Union[None, Unset, int]):
    """

    active_sw: str
    endpoint_uuid: str
    endpoint_user_name: str
    certificate_dn: str
    description: str
    uudex_administrator_sw: str
    participant_administrator_sw: str
    participant_id: int
    create_datetime: Union[Unset, datetime.datetime] = UNSET
    endpoint_id: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        active_sw = self.active_sw

        endpoint_uuid = self.endpoint_uuid

        endpoint_user_name = self.endpoint_user_name

        certificate_dn = self.certificate_dn

        description = self.description

        uudex_administrator_sw = self.uudex_administrator_sw

        participant_administrator_sw = self.participant_administrator_sw

        participant_id = self.participant_id

        create_datetime: Union[Unset, str] = UNSET
        if not isinstance(self.create_datetime, Unset):
            create_datetime = self.create_datetime.isoformat()

        endpoint_id: Union[None, Unset, int]
        if isinstance(self.endpoint_id, Unset):
            endpoint_id = UNSET
        else:
            endpoint_id = self.endpoint_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "active_sw": active_sw,
                "endpoint_uuid": endpoint_uuid,
                "endpoint_user_name": endpoint_user_name,
                "certificate_dn": certificate_dn,
                "description": description,
                "uudex_administrator_sw": uudex_administrator_sw,
                "participant_administrator_sw": participant_administrator_sw,
                "participant_id": participant_id,
            }
        )
        if create_datetime is not UNSET:
            field_dict["create_datetime"] = create_datetime
        if endpoint_id is not UNSET:
            field_dict["endpoint_id"] = endpoint_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        active_sw = d.pop("active_sw")

        endpoint_uuid = d.pop("endpoint_uuid")

        endpoint_user_name = d.pop("endpoint_user_name")

        certificate_dn = d.pop("certificate_dn")

        description = d.pop("description")

        uudex_administrator_sw = d.pop("uudex_administrator_sw")

        participant_administrator_sw = d.pop("participant_administrator_sw")

        participant_id = d.pop("participant_id")

        _create_datetime = d.pop("create_datetime", UNSET)
        create_datetime: Union[Unset, datetime.datetime]
        if isinstance(_create_datetime, Unset):
            create_datetime = UNSET
        else:
            create_datetime = isoparse(_create_datetime)

        def _parse_endpoint_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        endpoint_id = _parse_endpoint_id(d.pop("endpoint_id", UNSET))

        end_point = cls(
            active_sw=active_sw,
            endpoint_uuid=endpoint_uuid,
            endpoint_user_name=endpoint_user_name,
            certificate_dn=certificate_dn,
            description=description,
            uudex_administrator_sw=uudex_administrator_sw,
            participant_administrator_sw=participant_administrator_sw,
            participant_id=participant_id,
            create_datetime=create_datetime,
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
