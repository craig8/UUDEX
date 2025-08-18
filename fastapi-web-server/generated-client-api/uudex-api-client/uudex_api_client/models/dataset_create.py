from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast, Union
from typing import Union






T = TypeVar("T", bound="DatasetCreate")


@_attrs_define
class DatasetCreate:
    """ 
        Attributes:
            dataset_name (str):
            description (str):
            properties (str):
            payload (str):
            payload_size (int):
            payload_md5_hash (str):
            payload_compression_algorithm (str):
            version_number (int):
            subject_id (int):
            dataset_uuid (Union[Unset, str]):
            owner_participant_id (Union[None, Unset, int]):
     """

    dataset_name: str
    description: str
    properties: str
    payload: str
    payload_size: int
    payload_md5_hash: str
    payload_compression_algorithm: str
    version_number: int
    subject_id: int
    dataset_uuid: Union[Unset, str] = UNSET
    owner_participant_id: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        dataset_name = self.dataset_name

        description = self.description

        properties = self.properties

        payload = self.payload

        payload_size = self.payload_size

        payload_md5_hash = self.payload_md5_hash

        payload_compression_algorithm = self.payload_compression_algorithm

        version_number = self.version_number

        subject_id = self.subject_id

        dataset_uuid = self.dataset_uuid

        owner_participant_id: Union[None, Unset, int]
        if isinstance(self.owner_participant_id, Unset):
            owner_participant_id = UNSET
        else:
            owner_participant_id = self.owner_participant_id


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "dataset_name": dataset_name,
            "description": description,
            "properties": properties,
            "payload": payload,
            "payload_size": payload_size,
            "payload_md5_hash": payload_md5_hash,
            "payload_compression_algorithm": payload_compression_algorithm,
            "version_number": version_number,
            "subject_id": subject_id,
        })
        if dataset_uuid is not UNSET:
            field_dict["dataset_uuid"] = dataset_uuid
        if owner_participant_id is not UNSET:
            field_dict["owner_participant_id"] = owner_participant_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dataset_name = d.pop("dataset_name")

        description = d.pop("description")

        properties = d.pop("properties")

        payload = d.pop("payload")

        payload_size = d.pop("payload_size")

        payload_md5_hash = d.pop("payload_md5_hash")

        payload_compression_algorithm = d.pop("payload_compression_algorithm")

        version_number = d.pop("version_number")

        subject_id = d.pop("subject_id")

        dataset_uuid = d.pop("dataset_uuid", UNSET)

        def _parse_owner_participant_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        owner_participant_id = _parse_owner_participant_id(d.pop("owner_participant_id", UNSET))


        dataset_create = cls(
            dataset_name=dataset_name,
            description=description,
            properties=properties,
            payload=payload,
            payload_size=payload_size,
            payload_md5_hash=payload_md5_hash,
            payload_compression_algorithm=payload_compression_algorithm,
            version_number=version_number,
            subject_id=subject_id,
            dataset_uuid=dataset_uuid,
            owner_participant_id=owner_participant_id,
        )

        dataset_create.additional_properties = d
        return dataset_create

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
