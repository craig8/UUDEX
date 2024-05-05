from datetime import datetime
from typing import Optional

from sqlmodel import Field

from uudex_server.models import BaseModel


class SubjectPolicyAclConstraint(BaseModel, table=True):
    subject_policy_acl_constraint_id: Optional[int] = Field(default=None, primary_key=True)
    subject_policy_id: int = Field(foreign_key="subject_policy.subject_policy_id",
                                   primary_key=True)
    privilege_allowed_id: int = Field(foreign_key="privilege_allowed.privilege_allowed_id",
                                      primary_key=True)
    grant_scope_id: int = Field(foreign_key="grant_scope.grant_scope_id", primary_key=True)


class PrivilegeAllowed(BaseModel, table=True):
    privilege_allowed_id: Optional[int] = Field(default=None, primary_key=True)
    privilege_allowed_name: str


class GrantScope(BaseModel, table=True):
    grant_scope_id: Optional[int] = Field(default=None, primary_key=True)
    grant_scope_name: str


class SubjectPolicyBase(BaseModel):
    subject_policy_uuid: str
    subject_policy_type: str
    subject_policy_type_sort: int
    action: str
    full_queue_behavior: str
    max_queue_size_kb: int
    max_message_count: int
    max_priority: int


class SubjectPolicy(SubjectPolicyBase, table=True):
    __tablename__ = 'subject_policy'

    subject_policy_id: Optional[int] = Field(default=None, primary_key=True)
    dataset_definition_id: int = Field(foreign_key="dataset_definition.dataset_definition_id",
                                       primary_key=True)
    target_participant_id: int = Field(foreign_key="participant.participant_id", primary_key=True)


class SubjectPolicyAdd(SubjectPolicyBase):
    pass


class SubjectAcl(BaseModel, table=True):
    subject_acl_id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: int = Field(foreign_key="subject.subject_id", primary_key=True)
    privilege_id: int = Field(foreign_key="privilege.privilege_id", primary_key=True)
    grant_scope_id: int = Field(foreign_key="grant_scope.grant_scope_id", primary_key=True)


class SubjectAclGrant(BaseModel, table=True):
    __tablename__ = "subject_acl_grant"

    subject_acl_id: int = Field(foreign_key="subject_acl.subject_acl_id", primary_key=True)
    participant_id: int = Field(foreign_key="participant.participant_id", primary_key=True)


class SubjectPolicyGrantAllowed(BaseModel, table=True):
    __tablename__ = "subject_policy_grant_allowed"

    subject_policy_acl_constraint_id: int = Field(
        foreign_key="subject_policy_acl_constraint.subject_policy_acl_constraint_id",
        primary_key=True)
    participant_id: int = Field(foreign_key="participant.participant_id", primary_key=True)


class Privilege(BaseModel, table=True):
    privilege_id: Optional[int] = Field(default=None, primary_key=True)
    privilege_name: str
