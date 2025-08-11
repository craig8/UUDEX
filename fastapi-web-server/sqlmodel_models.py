from __future__ import annotations
# SQLModel models generated from database schema

from typing import Optional, List, Dict, Any
from sqlmodel import Field, SQLModel, Relationship
import datetime
from uuid import UUID


class AuthGroup(SQLModel, table=True):
    __tablename__ = "auth_group"    # type: ignore

    group_id: int = Field(
        primary_key=True,
        default=None,
    )
    group_uuid: str = Field(nullable=False, )
    group_name: str = Field(
        nullable=False,
        max_length=40,
    )
    description: Optional[str] = Field(max_length=255, )
    create_datetime: datetime.datetime = Field(nullable=False, )


class AuthRole(SQLModel, table=True):
    __tablename__ = "auth_role"    # type: ignore

    role_id: int = Field(
        primary_key=True,
        default=None,
    )
    role_uuid: str = Field(nullable=False, )
    role_name: str = Field(
        nullable=False,
        max_length=40,
    )
    description: Optional[str] = Field(max_length=255, )
    create_datetime: datetime.datetime = Field(nullable=False, )


class Contact(SQLModel, table=True):
    __tablename__ = "contact"    # type: ignore

    contact_id: int = Field(
        primary_key=True,
        default=None,
    )
    contact_name: str = Field(
        nullable=False,
        max_length=30,
    )
    contact_number: str = Field(
        nullable=False,
        max_length=15,
    )
    participant_id: int = Field(nullable=False, )


class Dataset(SQLModel, table=True):
    __tablename__ = "dataset"    # type: ignore

    dataset_id: int = Field(
        primary_key=True,
        default=None,
    )
    dataset_uuid: str = Field(nullable=False, )
    dataset_name: str = Field(
        nullable=False,
        max_length=255,
    )
    description: str = Field(
        nullable=False,
        max_length=255,
    )
    properties: Optional[str] = Field(max_length=1024, )
    payload: bytes = Field(nullable=False, )
    payload_size: int = Field(nullable=False, )
    payload_md5_hash: str = Field(nullable=False, )
    payload_compression_algorithm: str = Field(
        nullable=False,
        max_length=15,
    )
    version_number: int = Field(nullable=False, )
    create_datetime: datetime.datetime = Field(nullable=False, )
    owner_participant_id: int = Field(nullable=False, )
    subject_id: int = Field(nullable=False, )


class DatasetDefinition(SQLModel, table=True):
    __tablename__ = "dataset_definition"    # type: ignore

    dataset_definition_id: int = Field(
        primary_key=True,
        default=None,
    )
    dataset_definition_uuid: str = Field(nullable=False, )
    dataset_definition_name: str = Field(
        nullable=False,
        max_length=100,
    )
    description: Optional[str] = Field(max_length=255, )
    create_datetime: datetime.datetime = Field(nullable=False, )


class Endpoint(SQLModel, table=True):
    __tablename__ = "endpoint"    # type: ignore

    endpoint_id: int = Field(
        primary_key=True,
        default=None,
    )
    endpoint_uuid: str = Field(nullable=False, )
    endpoint_user_name: str = Field(
        nullable=False,
        max_length=30,
    )
    certificate_dn: str = Field(
        nullable=False,
        max_length=255,
    )
    description: Optional[str] = Field(max_length=255, )
    active_sw: str = Field(nullable=False, )
    create_datetime: datetime.datetime = Field(nullable=False, )
    participant_id: int = Field(nullable=False, )


class GrantScope(SQLModel, table=True):
    __tablename__ = "grant_scope"    # type: ignore

    grant_scope_id: int = Field(primary_key=True, )
    grant_scope_name: Optional[str] = Field(max_length=40, )


class Participant(SQLModel, table=True):
    __tablename__ = "participant"    # type: ignore

    participant_id: int = Field(
        primary_key=True,
        default=None,
    )
    participant_uuid: str = Field(nullable=False, )
    participant_short_name: str = Field(
        nullable=False,
        max_length=25,
    )
    participant_long_name: str = Field(
        nullable=False,
        max_length=50,
    )
    description: Optional[str] = Field(max_length=255, )
    root_org_sw: str = Field(nullable=False, )
    active_sw: str = Field(nullable=False, )
    create_datetime: datetime.datetime = Field(nullable=False, )


class PrivilegeAllowed(SQLModel, table=True):
    __tablename__ = "privilege_allowed"    # type: ignore

    privilege_allowed_id: int = Field(primary_key=True, )
    privilege_allowed_name: Optional[str] = Field(max_length=40, )


class Subject(SQLModel, table=True):
    __tablename__ = "subject"    # type: ignore

    subject_id: int = Field(
        primary_key=True,
        default=None,
    )
    subject_uuid: str = Field(nullable=False, )
    subject_name: str = Field(
        nullable=False,
        max_length=300,
    )
    dataset_instance_key: str = Field(
        nullable=False,
        max_length=100,
    )
    description: Optional[str] = Field(max_length=300, )
    subscription_type: str = Field(nullable=False, )
    fulfillment_types_available: str = Field(
        nullable=False,
        max_length=15,
    )
    full_queue_behavior: Optional[str] = Field(max_length=20, )
    max_queue_size_kb: Optional[int] = Field()
    max_message_count: Optional[int] = Field()
    priority: Optional[int] = Field()
    backing_exchange_name: Optional[str] = Field(max_length=300, )
    create_datetime: datetime.datetime = Field(nullable=False, )
    owner_participant_id: int = Field(nullable=False, )
    dataset_definition_id: int = Field(nullable=False, )


class SubjectPolicy(SQLModel, table=True):
    __tablename__ = "subject_policy"    # type: ignore

    subject_policy_id: int = Field(
        primary_key=True,
        default=None,
    )
    subject_policy_uuid: str = Field(nullable=False, )
    subject_policy_type: str = Field(
        nullable=False,
        max_length=25,
    )
    subject_policy_type_sort: int = Field(nullable=False, )
    action: str = Field(
        nullable=False,
        max_length=10,
    )
    full_queue_behavior: Optional[str] = Field(max_length=20, )
    max_queue_size_kb: Optional[int] = Field()
    max_message_count: Optional[int] = Field()
    max_priority: Optional[int] = Field()
    target_participant_id: Optional[int] = Field()
    dataset_definition_id: Optional[int] = Field()


class SubjectPolicyAclConstraint(SQLModel, table=True):
    __tablename__ = "subject_policy_acl_constraint"    # type: ignore

    subject_policy_acl_constraint_id: int = Field(
        primary_key=True,
        default=None,
    )
    subject_policy_id: int = Field(nullable=False, )
    privilege_allowed_id: int = Field(nullable=False, )
    grant_scope_id: int = Field(nullable=False, )


class SubjectPolicyGrantAllowed(SQLModel, table=True):
    __tablename__ = "subject_policy_grant_allowed"    # type: ignore

    sp_grant_allowed_id: int = Field(
        primary_key=True,
        default=None,
    )
    object_uuid: str = Field(nullable=False, )
    object_type: str = Field(nullable=False, )
    create_datetime: datetime.datetime = Field(nullable=False, )
    subject_policy_acl_constraint_id: int = Field(nullable=False, )


class Subscription(SQLModel, table=True):
    __tablename__ = "subscription"    # type: ignore

    subscription_id: int = Field(
        primary_key=True,
        default=None,
    )
    subscription_uuid: str = Field(nullable=False, )
    subscription_name: str = Field(
        nullable=False,
        max_length=30,
    )
    subscription_state: str = Field(
        nullable=False,
        max_length=10,
    )
    create_datetime: datetime.datetime = Field(nullable=False, )
    owner_endpoint_id: int = Field(nullable=False, )


class SubscriptionSubject(SQLModel, table=True):
    __tablename__ = "subscription_subject"    # type: ignore

    subscription_subject_id: int = Field(
        primary_key=True,
        default=None,
    )
    preferred_fulfillment_type: str = Field(
        nullable=False,
        max_length=15,
    )
    backing_queue_name: Optional[str] = Field(max_length=255, )
    subject_id: int = Field(nullable=False, )
    subscription_id: int = Field(nullable=False, )


# API models for request/response operations


class AuthGroupCreate(SQLModel):
    group_uuid: str
    group_name: str
    description: Optional[str] = None
    create_datetime: datetime.datetime


class AuthGroupRead(SQLModel):
    group_id: int
    group_uuid: str
    group_name: str
    description: str
    create_datetime: datetime.datetime


class AuthGroupUpdate(SQLModel):
    group_uuid: Optional[str] = None
    group_name: Optional[str] = None
    description: Optional[str] = None
    create_datetime: Optional[datetime.datetime] = None


class AuthRoleCreate(SQLModel):
    role_uuid: str
    role_name: str
    description: Optional[str] = None
    create_datetime: datetime.datetime


class AuthRoleRead(SQLModel):
    role_id: int
    role_uuid: str
    role_name: str
    description: str
    create_datetime: datetime.datetime


class AuthRoleUpdate(SQLModel):
    role_uuid: Optional[str] = None
    role_name: Optional[str] = None
    description: Optional[str] = None
    create_datetime: Optional[datetime.datetime] = None


class ContactCreate(SQLModel):
    contact_name: str
    contact_number: str
    participant_id: int


class ContactRead(SQLModel):
    contact_id: int
    contact_name: str
    contact_number: str
    participant_id: int


class ContactUpdate(SQLModel):
    contact_name: Optional[str] = None
    contact_number: Optional[str] = None
    participant_id: Optional[int] = None


class DatasetCreate(SQLModel):
    dataset_uuid: str
    dataset_name: str
    description: str
    properties: Optional[str] = None
    payload: bytes
    payload_size: int
    payload_md5_hash: str
    payload_compression_algorithm: str
    version_number: int
    create_datetime: datetime.datetime
    owner_participant_id: int
    subject_id: int


class DatasetRead(SQLModel):
    dataset_id: int
    dataset_uuid: str
    dataset_name: str
    description: str
    properties: str
    payload: bytes
    payload_size: int
    payload_md5_hash: str
    payload_compression_algorithm: str
    version_number: int
    create_datetime: datetime.datetime
    owner_participant_id: int
    subject_id: int


class DatasetUpdate(SQLModel):
    dataset_uuid: Optional[str] = None
    dataset_name: Optional[str] = None
    description: Optional[str] = None
    properties: Optional[str] = None
    payload: Optional[bytes] = None
    payload_size: Optional[int] = None
    payload_md5_hash: Optional[str] = None
    payload_compression_algorithm: Optional[str] = None
    version_number: Optional[int] = None
    create_datetime: Optional[datetime.datetime] = None
    owner_participant_id: Optional[int] = None
    subject_id: Optional[int] = None


class DatasetDefinitionCreate(SQLModel):
    dataset_definition_uuid: str
    dataset_definition_name: str
    description: Optional[str] = None
    create_datetime: datetime.datetime


class DatasetDefinitionRead(SQLModel):
    dataset_definition_id: int
    dataset_definition_uuid: str
    dataset_definition_name: str
    description: str
    create_datetime: datetime.datetime


class DatasetDefinitionUpdate(SQLModel):
    dataset_definition_uuid: Optional[str] = None
    dataset_definition_name: Optional[str] = None
    description: Optional[str] = None
    create_datetime: Optional[datetime.datetime] = None


class EndpointCreate(SQLModel):
    endpoint_uuid: str
    endpoint_user_name: str
    certificate_dn: str
    description: Optional[str] = None
    active_sw: str
    create_datetime: datetime.datetime
    participant_id: int


class EndpointRead(SQLModel):
    endpoint_id: int
    endpoint_uuid: str
    endpoint_user_name: str
    certificate_dn: str
    description: str
    active_sw: str
    create_datetime: datetime.datetime
    participant_id: int


class EndpointUpdate(SQLModel):
    endpoint_uuid: Optional[str] = None
    endpoint_user_name: Optional[str] = None
    certificate_dn: Optional[str] = None
    description: Optional[str] = None
    active_sw: Optional[str] = None
    create_datetime: Optional[datetime.datetime] = None
    participant_id: Optional[int] = None


class GrantScopeCreate(SQLModel):
    grant_scope_id: int
    grant_scope_name: Optional[str] = None


class GrantScopeRead(SQLModel):
    grant_scope_id: int
    grant_scope_name: str


class GrantScopeUpdate(SQLModel):
    grant_scope_name: Optional[str] = None


class ParticipantCreate(SQLModel):
    participant_uuid: str
    participant_short_name: str
    participant_long_name: str
    description: Optional[str] = None
    root_org_sw: str
    active_sw: str
    create_datetime: datetime.datetime


class ParticipantRead(SQLModel):
    participant_id: int
    participant_uuid: str
    participant_short_name: str
    participant_long_name: str
    description: str
    root_org_sw: str
    active_sw: str
    create_datetime: datetime.datetime


class ParticipantUpdate(SQLModel):
    participant_uuid: Optional[str] = None
    participant_short_name: Optional[str] = None
    participant_long_name: Optional[str] = None
    description: Optional[str] = None
    root_org_sw: Optional[str] = None
    active_sw: Optional[str] = None
    create_datetime: Optional[datetime.datetime] = None


class PrivilegeAllowedCreate(SQLModel):
    privilege_allowed_id: int
    privilege_allowed_name: Optional[str] = None


class PrivilegeAllowedRead(SQLModel):
    privilege_allowed_id: int
    privilege_allowed_name: str


class PrivilegeAllowedUpdate(SQLModel):
    privilege_allowed_name: Optional[str] = None


class SubjectCreate(SQLModel):
    subject_uuid: str
    subject_name: str
    dataset_instance_key: str
    description: Optional[str] = None
    subscription_type: str
    fulfillment_types_available: str
    full_queue_behavior: Optional[str] = None
    max_queue_size_kb: Optional[int] = None
    max_message_count: Optional[int] = None
    priority: Optional[int] = None
    backing_exchange_name: Optional[str] = None
    create_datetime: datetime.datetime
    owner_participant_id: int
    dataset_definition_id: int


class SubjectRead(SQLModel):
    subject_id: int
    subject_uuid: str
    subject_name: str
    dataset_instance_key: str
    description: str
    subscription_type: str
    fulfillment_types_available: str
    full_queue_behavior: str
    max_queue_size_kb: int
    max_message_count: int
    priority: int
    backing_exchange_name: str
    create_datetime: datetime.datetime
    owner_participant_id: int
    dataset_definition_id: int


class SubjectUpdate(SQLModel):
    subject_uuid: Optional[str] = None
    subject_name: Optional[str] = None
    dataset_instance_key: Optional[str] = None
    description: Optional[str] = None
    subscription_type: Optional[str] = None
    fulfillment_types_available: Optional[str] = None
    full_queue_behavior: Optional[str] = None
    max_queue_size_kb: Optional[int] = None
    max_message_count: Optional[int] = None
    priority: Optional[int] = None
    backing_exchange_name: Optional[str] = None
    create_datetime: Optional[datetime.datetime] = None
    owner_participant_id: Optional[int] = None
    dataset_definition_id: Optional[int] = None


class SubjectPolicyCreate(SQLModel):
    subject_policy_uuid: str
    subject_policy_type: str
    subject_policy_type_sort: int
    action: str
    full_queue_behavior: Optional[str] = None
    max_queue_size_kb: Optional[int] = None
    max_message_count: Optional[int] = None
    max_priority: Optional[int] = None
    target_participant_id: Optional[int] = None
    dataset_definition_id: Optional[int] = None


class SubjectPolicyRead(SQLModel):
    subject_policy_id: int
    subject_policy_uuid: str
    subject_policy_type: str
    subject_policy_type_sort: int
    action: str
    full_queue_behavior: str
    max_queue_size_kb: int
    max_message_count: int
    max_priority: int
    target_participant_id: int
    dataset_definition_id: int


class SubjectPolicyUpdate(SQLModel):
    subject_policy_uuid: Optional[str] = None
    subject_policy_type: Optional[str] = None
    subject_policy_type_sort: Optional[int] = None
    action: Optional[str] = None
    full_queue_behavior: Optional[str] = None
    max_queue_size_kb: Optional[int] = None
    max_message_count: Optional[int] = None
    max_priority: Optional[int] = None
    target_participant_id: Optional[int] = None
    dataset_definition_id: Optional[int] = None


class SubjectPolicyAclConstraintCreate(SQLModel):
    subject_policy_id: int
    privilege_allowed_id: int
    grant_scope_id: int


class SubjectPolicyAclConstraintRead(SQLModel):
    subject_policy_acl_constraint_id: int
    subject_policy_id: int
    privilege_allowed_id: int
    grant_scope_id: int


class SubjectPolicyAclConstraintUpdate(SQLModel):
    subject_policy_id: Optional[int] = None
    privilege_allowed_id: Optional[int] = None
    grant_scope_id: Optional[int] = None


class SubjectPolicyGrantAllowedCreate(SQLModel):
    object_uuid: str
    object_type: str
    create_datetime: datetime.datetime
    subject_policy_acl_constraint_id: int


class SubjectPolicyGrantAllowedRead(SQLModel):
    sp_grant_allowed_id: int
    object_uuid: str
    object_type: str
    create_datetime: datetime.datetime
    subject_policy_acl_constraint_id: int


class SubjectPolicyGrantAllowedUpdate(SQLModel):
    object_uuid: Optional[str] = None
    object_type: Optional[str] = None
    create_datetime: Optional[datetime.datetime] = None
    subject_policy_acl_constraint_id: Optional[int] = None


class SubscriptionCreate(SQLModel):
    subscription_uuid: str
    subscription_name: str
    subscription_state: str
    create_datetime: datetime.datetime
    owner_endpoint_id: int


class SubscriptionRead(SQLModel):
    subscription_id: int
    subscription_uuid: str
    subscription_name: str
    subscription_state: str
    create_datetime: datetime.datetime
    owner_endpoint_id: int


class SubscriptionUpdate(SQLModel):
    subscription_uuid: Optional[str] = None
    subscription_name: Optional[str] = None
    subscription_state: Optional[str] = None
    create_datetime: Optional[datetime.datetime] = None
    owner_endpoint_id: Optional[int] = None


class SubscriptionSubjectCreate(SQLModel):
    preferred_fulfillment_type: str
    backing_queue_name: Optional[str] = None
    subject_id: int
    subscription_id: int


class SubscriptionSubjectRead(SQLModel):
    subscription_subject_id: int
    preferred_fulfillment_type: str
    backing_queue_name: str
    subject_id: int
    subscription_id: int


class SubscriptionSubjectUpdate(SQLModel):
    preferred_fulfillment_type: Optional[str] = None
    backing_queue_name: Optional[str] = None
    subject_id: Optional[int] = None
    subscription_id: Optional[int] = None
