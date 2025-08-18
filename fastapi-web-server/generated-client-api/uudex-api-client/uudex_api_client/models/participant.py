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






T = TypeVar("T", bound="Participant")


@_attrs_define
class Participant:
    """ 
        Attributes:
            create_datetime (Union[None, datetime.datetime]):
            participant_uuid (str):
            participant_short_name (str):
            participant_long_name (str):
            root_org_sw (str):
            active_sw (Union[Unset, str]):  Default: 'Y'.
            description (Union[None, Unset, str]):
            participant_id (Union[None, Unset, int]):
     """

    create_datetime: Union[None, datetime.datetime]
    participant_uuid: str
    participant_short_name: str
    participant_long_name: str
    root_org_sw: str
    active_sw: Union[Unset, str] = 'Y'
    description: Union[None, Unset, str] = UNSET
    participant_id: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        create_datetime: Union[None, str]
        if isinstance(self.create_datetime, datetime.datetime):
            create_datetime = self.create_datetime.isoformat()
        else:
            create_datetime = self.create_datetime

        participant_uuid = self.participant_uuid

        participant_short_name = self.participant_short_name

        participant_long_name = self.participant_long_name

        root_org_sw = self.root_org_sw

        active_sw = self.active_sw

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        participant_id: Union[None, Unset, int]
        if isinstance(self.participant_id, Unset):
            participant_id = UNSET
        else:
            participant_id = self.participant_id


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "create_datetime": create_datetime,
            "participant_uuid": participant_uuid,
            "participant_short_name": participant_short_name,
            "participant_long_name": participant_long_name,
            "root_org_sw": root_org_sw,
        })
        if active_sw is not UNSET:
            field_dict["active_sw"] = active_sw
        if description is not UNSET:
            field_dict["description"] = description
        if participant_id is not UNSET:
            field_dict["participant_id"] = participant_id

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


        participant_uuid = d.pop("participant_uuid")

        participant_short_name = d.pop("participant_short_name")

        participant_long_name = d.pop("participant_long_name")

        root_org_sw = d.pop("root_org_sw")

        active_sw = d.pop("active_sw", UNSET)

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))


        def _parse_participant_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        participant_id = _parse_participant_id(d.pop("participant_id", UNSET))


        participant = cls(
            create_datetime=create_datetime,
            participant_uuid=participant_uuid,
            participant_short_name=participant_short_name,
            participant_long_name=participant_long_name,
            root_org_sw=root_org_sw,
            active_sw=active_sw,
            description=description,
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
