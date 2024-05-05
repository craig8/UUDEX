import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Participant")


@_attrs_define
class Participant:
    """
    Attributes:
        active_sw (str):
        participant_uuid (str):
        participant_short_name (str):
        participant_long_name (str):
        description (str):
        root_org_sw (str):
        create_datetime (Union[Unset, datetime.datetime]):
        participant_id (Union[None, Unset, int]):
    """

    active_sw: str
    participant_uuid: str
    participant_short_name: str
    participant_long_name: str
    description: str
    root_org_sw: str
    create_datetime: Union[Unset, datetime.datetime] = UNSET
    participant_id: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        active_sw = self.active_sw

        participant_uuid = self.participant_uuid

        participant_short_name = self.participant_short_name

        participant_long_name = self.participant_long_name

        description = self.description

        root_org_sw = self.root_org_sw

        create_datetime: Union[Unset, str] = UNSET
        if not isinstance(self.create_datetime, Unset):
            create_datetime = self.create_datetime.isoformat()

        participant_id: Union[None, Unset, int]
        if isinstance(self.participant_id, Unset):
            participant_id = UNSET
        else:
            participant_id = self.participant_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "active_sw": active_sw,
                "participant_uuid": participant_uuid,
                "participant_short_name": participant_short_name,
                "participant_long_name": participant_long_name,
                "description": description,
                "root_org_sw": root_org_sw,
            }
        )
        if create_datetime is not UNSET:
            field_dict["create_datetime"] = create_datetime
        if participant_id is not UNSET:
            field_dict["participant_id"] = participant_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        active_sw = d.pop("active_sw")

        participant_uuid = d.pop("participant_uuid")

        participant_short_name = d.pop("participant_short_name")

        participant_long_name = d.pop("participant_long_name")

        description = d.pop("description")

        root_org_sw = d.pop("root_org_sw")

        _create_datetime = d.pop("create_datetime", UNSET)
        create_datetime: Union[Unset, datetime.datetime]
        if isinstance(_create_datetime, Unset):
            create_datetime = UNSET
        else:
            create_datetime = isoparse(_create_datetime)

        def _parse_participant_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        participant_id = _parse_participant_id(d.pop("participant_id", UNSET))

        participant = cls(
            active_sw=active_sw,
            participant_uuid=participant_uuid,
            participant_short_name=participant_short_name,
            participant_long_name=participant_long_name,
            description=description,
            root_org_sw=root_org_sw,
            create_datetime=create_datetime,
            participant_id=participant_id,
        )

        participant.additional_properties = d
        return participant

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
