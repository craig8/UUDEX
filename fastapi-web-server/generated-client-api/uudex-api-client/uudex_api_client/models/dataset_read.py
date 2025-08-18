from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from dateutil.parser import isoparse
from typing import cast
from ..types import UNSET, Unset
import datetime
from typing import cast, Union






T = TypeVar("T", bound="DatasetRead")


@_attrs_define
class DatasetRead:
    """ Dataset metadata without payload for efficient listing/browsing

        Attributes:
            dataset_id (int):
            dataset_uuid (str):
            dataset_name (str):
            description (str):
            payload_size (int):
            payload_md5_hash (str):
            payload_compression_algorithm (str):
            version_number (int):
            owner_participant_id (int):
            subject_id (int):
            create_datetime (datetime.datetime):
            properties (Union[None, Unset, str]):
     """

    dataset_id: int
    dataset_uuid: str
    dataset_name: str
    description: str
    payload_size: int
    payload_md5_hash: str
    payload_compression_algorithm: str
    version_number: int
    owner_participant_id: int
    subject_id: int
    create_datetime: datetime.datetime
    properties: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        dataset_id = self.dataset_id

        dataset_uuid = self.dataset_uuid

        dataset_name = self.dataset_name

        description = self.description

        payload_size = self.payload_size

        payload_md5_hash = self.payload_md5_hash

        payload_compression_algorithm = self.payload_compression_algorithm

        version_number = self.version_number

        owner_participant_id = self.owner_participant_id

        subject_id = self.subject_id

        create_datetime = self.create_datetime.isoformat()

        properties: Union[None, Unset, str]
        if isinstance(self.properties, Unset):
            properties = UNSET
        else:
            properties = self.properties


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "dataset_id": dataset_id,
            "dataset_uuid": dataset_uuid,
            "dataset_name": dataset_name,
            "description": description,
            "payload_size": payload_size,
            "payload_md5_hash": payload_md5_hash,
            "payload_compression_algorithm": payload_compression_algorithm,
            "version_number": version_number,
            "owner_participant_id": owner_participant_id,
            "subject_id": subject_id,
            "create_datetime": create_datetime,
        })
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dataset_id = d.pop("dataset_id")

        dataset_uuid = d.pop("dataset_uuid")

        dataset_name = d.pop("dataset_name")

        description = d.pop("description")

        payload_size = d.pop("payload_size")

        payload_md5_hash = d.pop("payload_md5_hash")

        payload_compression_algorithm = d.pop("payload_compression_algorithm")

        version_number = d.pop("version_number")

        owner_participant_id = d.pop("owner_participant_id")

        subject_id = d.pop("subject_id")

        create_datetime = isoparse(d.pop("create_datetime"))




        def _parse_properties(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        properties = _parse_properties(d.pop("properties", UNSET))


        dataset_read = cls(
            dataset_id=dataset_id,
            dataset_uuid=dataset_uuid,
            dataset_name=dataset_name,
            description=description,
            payload_size=payload_size,
            payload_md5_hash=payload_md5_hash,
            payload_compression_algorithm=payload_compression_algorithm,
            version_number=version_number,
            owner_participant_id=owner_participant_id,
            subject_id=subject_id,
            create_datetime=create_datetime,
            properties=properties,
        )

        dataset_read.additional_properties = d
        return dataset_read

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
