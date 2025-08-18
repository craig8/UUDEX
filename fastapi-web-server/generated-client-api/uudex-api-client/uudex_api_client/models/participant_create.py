from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from ..types import UNSET, Unset
from typing import cast, Union






T = TypeVar("T", bound="ParticipantCreate")


@_attrs_define
class ParticipantCreate:
    """ 
        Attributes:
            participant_uuid (str):
            participant_short_name (str):
            participant_long_name (str):
            root_org_sw (str):
            description (Union[None, Unset, str]):
            active_sw (Union[Unset, str]):  Default: 'Y'.
     """

    participant_uuid: str
    participant_short_name: str
    participant_long_name: str
    root_org_sw: str
    description: Union[None, Unset, str] = UNSET
    active_sw: Union[Unset, str] = 'Y'
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        participant_uuid = self.participant_uuid

        participant_short_name = self.participant_short_name

        participant_long_name = self.participant_long_name

        root_org_sw = self.root_org_sw

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        active_sw = self.active_sw


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "participant_uuid": participant_uuid,
            "participant_short_name": participant_short_name,
            "participant_long_name": participant_long_name,
            "root_org_sw": root_org_sw,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if active_sw is not UNSET:
            field_dict["active_sw"] = active_sw

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        participant_uuid = d.pop("participant_uuid")

        participant_short_name = d.pop("participant_short_name")

        participant_long_name = d.pop("participant_long_name")

        root_org_sw = d.pop("root_org_sw")

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))


        active_sw = d.pop("active_sw", UNSET)

        participant_create = cls(
            participant_uuid=participant_uuid,
            participant_short_name=participant_short_name,
            participant_long_name=participant_long_name,
            root_org_sw=root_org_sw,
            description=description,
            active_sw=active_sw,
        )

        participant_create.additional_properties = d
        return participant_create

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
