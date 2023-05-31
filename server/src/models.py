"""

UUDEX

Copyright © 2021, Battelle Memorial Institute

1. Battelle Memorial Institute (hereinafter Battelle) hereby grants
permission to any person or entity lawfully obtaining a copy of this
software and associated documentation files (hereinafter “the Software”)
to redistribute and use the Software in source and binary forms, with or
without modification.  Such person or entity may use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software, and
may permit others to do so, subject to the following conditions:

   - Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimers.
   - Redistributions in binary form must reproduce the above copyright notice,
     this list of conditions and the following disclaimer in the documentation
     and/or other materials provided with the distribution.
   - Other than as used herein, neither the name Battelle Memorial Institute
     or Battelle may be used in any form whatsoever without the express
     written consent of Battelle.

2. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL BATTELLE OR CONTRIBUTORS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

import datetime
from uuid import uuid4
#
from sqlalchemy.orm import backref
from uudex_model_base import db

class AuthGroup(db.Model):
    __tablename__ = 'auth_group'

    group_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    group_uuid = db.Column(db.String(36), nullable=False, unique=True, default=lambda: uuid4())
    group_name = db.Column(db.String(40), nullable=False)
    description  = db.Column(db.String(255))
    create_datetime = db.Column(db.DateTime(True), nullable=False, default=datetime.datetime.utcnow)

class AuthRole(db.Model):
    __tablename__ = 'auth_role'

    role_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    role_uuid = db.Column(db.String(36), nullable=False, unique=True, default=lambda: uuid4())
    role_name = db.Column(db.String(40), nullable=False)
    description  = db.Column(db.String(255))
    create_datetime = db.Column(db.DateTime(True), nullable=False, default=datetime.datetime.utcnow)


class Contact(db.Model):
    __tablename__ = 'contact'

    contact_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    contact_name = db.Column(db.String(30), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    participant_id = db.Column(db.ForeignKey('participant.participant_id', ondelete='CASCADE'), nullable=False, index=True)

    participant = db.relationship('Participant', primaryjoin='Contact.participant_id == Participant.participant_id', backref='contacts')


class DatasetDefinition(db.Model):
    __tablename__ = 'dataset_definition'

    dataset_definition_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    dataset_definition_uuid = db.Column(db.String(36), nullable=False, unique=True, default=lambda: uuid4())
    dataset_definition_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    schema = db.Column(db.String(32 * 1024))
    create_datetime = db.Column(db.DateTime(True), nullable=False, default=datetime.datetime.utcnow)



class Dataset(db.Model):
    __tablename__ = 'dataset'
    __table_args__ = (
        db.CheckConstraint(
            "(payload_compression_algorithm)::text = ANY ((ARRAY['LZMA'::character varying, 'NONE'::character varying, 'AVRO'::character varying])::text[])"),
    )

    dataset_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    dataset_uuid = db.Column(db.String(36), nullable=False, unique=True, default=lambda: uuid4())
    dataset_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    properties = db.Column(db.String(1024))
    payload = db.Column(db.LargeBinary, nullable=False)
    payload_size = db.Column(db.Integer, nullable=False)
    payload_md5_hash = db.Column(db.String(32), nullable=False)
    payload_compression_algorithm = db.Column(db.String(15), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    create_datetime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    owner_participant_id = db.Column(db.ForeignKey('participant.participant_id'), nullable=False, index=True)
    subject_id = db.Column(db.ForeignKey('subject.subject_id'), nullable=False, index=True)

    owner_participant = db.relationship('Participant', primaryjoin='Dataset.owner_participant_id == Participant.participant_id', backref='datasets')
    subject = db.relationship('Subject', primaryjoin='Dataset.subject_id == Subject.subject_id', backref='datasets')


class Endpoint(db.Model):
    __tablename__ = 'endpoint'
    __table_args__ = (
        db.CheckConstraint("upper((active_sw)::text) = ANY (ARRAY['Y'::text, 'N'::text])"),
    )

    endpoint_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    endpoint_uuid = db.Column(db.String(36), nullable=False, unique=True, default=lambda: uuid4())
    endpoint_user_name = db.Column(db.String(30), nullable=False)
    certificate_dn = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(255))
    active_sw = db.Column(db.String(1), nullable=False)
    create_datetime = db.Column(db.DateTime(True), nullable=False, default=datetime.datetime.utcnow)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.participant_id', ondelete='CASCADE'), nullable=False, index=True)

    #participant = db.relationship('Participant', primaryjoin='Endpoint.participant_id == Participant.participant_id',
    participant = db.relationship('Participant', primaryjoin='Endpoint.participant_id == Participant.participant_id',
                                  backref=backref('endpoints', passive_deletes=True))



class GrantScope(db.Model):
    __tablename__ = 'grant_scope'
    __table_args__ = (
        db.CheckConstraint("upper((grant_scope_name)::text) = ANY (ARRAY['ALLOW_ONLY'::text, 'ALLOW_EXCEPT'::text, 'ALLOW_ALL'::text, 'ALLOW_NONE'::text])"),
    )

    grant_scope_id = db.Column(db.Integer, primary_key=True)
    grant_scope_name = db.Column(db.String(40))



class Participant(db.Model):
    __tablename__ = 'participant'
    __table_args__ = (
        db.CheckConstraint("active_sw = ANY (ARRAY['Y'::bpchar, 'N'::bpchar])"),
    )

    participant_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    participant_uuid = db.Column(db.String(36), nullable=False, unique=True, default=lambda: uuid4())
    participant_short_name = db.Column(db.String(25), nullable=False)
    participant_long_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    active_sw = db.Column(db.String(1), nullable=False)
    create_datetime = db.Column(db.DateTime(True), nullable=False, default=datetime.datetime.utcnow)


class PrivilegeAllowed(db.Model):
    __tablename__ = 'privilege_allowed'
    __table_args__ = (
        db.CheckConstraint("upper((privilege_allowed_name)::text) = ANY (ARRAY['BROADEST_ALLOWED_PUBLISHER_ACCESS'::text, 'BROADEST_ALLOWED_SUBSCRIBER_ACCESS'::text, 'BROADEST_ALLOWED_MANAGER_ACCESS'::text])"),
    )

    privilege_allowed_id = db.Column(db.Integer, primary_key=True)
    privilege_allowed_name = db.Column(db.String(40))


class Subject(db.Model):
    __tablename__ = 'subject'
    __table_args__ = (
        db.CheckConstraint("upper((fulfillment_types_available)::text) = ANY (ARRAY['DATA_PUSH'::text, 'DATA_NOTIFY'::text, 'BOTH'::text])"),
        db.CheckConstraint("upper((full_queue_behavior)::text) = ANY (ARRAY['BLOCK_NEW'::text, 'PURGE_OLD'::text, 'NO_CONSTRAINT'::text])"),
        db.CheckConstraint("upper((subscription_type)::text) = ANY (ARRAY['MEASUREMENT_VALUES'::text, 'EVENT'::text])")
    )

    subject_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    subject_uuid = db.Column(db.String(36), nullable=False, unique=True, default=lambda: uuid4())
    subject_name = db.Column(db.String(300), nullable=False, unique=True)
    dataset_instance_key = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))
    subscription_type = db.Column(db.String(20), nullable=False)
    fulfillment_types_available = db.Column(db.String(15), nullable=False)
    full_queue_behavior = db.Column(db.String(20))
    max_queue_size_kb = db.Column(db.Integer)
    max_message_count = db.Column(db.Integer)
    priority = db.Column(db.Integer)
    backing_exchange_name = db.Column(db.String(300))
    create_datetime = db.Column(db.DateTime(True), nullable=False, default=datetime.datetime.utcnow)
    owner_participant_id = db.Column(db.ForeignKey('participant.participant_id'), nullable=False, index=True)
    dataset_definition_id = db.Column(db.ForeignKey('dataset_definition.dataset_definition_id'), nullable=False, index=True)

    dataset_definition = db.relationship('DatasetDefinition', primaryjoin='Subject.dataset_definition_id == DatasetDefinition.dataset_definition_id', backref='subjects')
    owner_participant = db.relationship('Participant', primaryjoin='Subject.owner_participant_id == Participant.participant_id', backref='subjects')


class SubjectPolicy(db.Model):
    __tablename__ = 'subject_policy'
    __table_args__ = (
        db.CheckConstraint('subject_policy_type_sort = ANY (ARRAY[1, 2, 3, 4])'),
        db.CheckConstraint("upper((action)::text) = ANY (ARRAY['ALLOW'::text, 'DENY'::text, 'REVIEW'::text])"),
        db.CheckConstraint("upper((full_queue_behavior)::text) = ANY (ARRAY['BLOCK_NEW'::text, 'PURGE_OLD'::text, 'NO_CONSTRAINT'::text])"),
        db.CheckConstraint("upper((subject_policy_type)::text) = ANY (ARRAY['PARTICIPANT_AND_DATASET'::text, 'PARTICIPANT'::text, 'DATASET'::text, 'GLOBAL_DEFAULT'::text])")
    )

    subject_policy_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    subject_policy_uuid = db.Column(db.String(36), nullable=False, unique=True, default=lambda: uuid4())
    subject_policy_type = db.Column(db.String(25), nullable=False)
    subject_policy_type_sort = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(10), nullable=False)
    full_queue_behavior = db.Column(db.String(20))
    max_queue_size_kb = db.Column(db.Integer)
    max_message_count = db.Column(db.Integer)
    max_priority = db.Column(db.Integer)
    target_participant_id = db.Column(db.ForeignKey('participant.participant_id'), index=True)
    dataset_definition_id = db.Column(db.ForeignKey('dataset_definition.dataset_definition_id', ondelete='CASCADE'), index=True)

    dataset_definition = db.relationship('DatasetDefinition', primaryjoin='SubjectPolicy.dataset_definition_id == DatasetDefinition.dataset_definition_id', backref='subject_policies')
    target_participant = db.relationship('Participant', primaryjoin='SubjectPolicy.target_participant_id == Participant.participant_id', backref='subject_policies')



class SubjectPolicyAclConstraint(db.Model):
    __tablename__ = 'subject_policy_acl_constraint'
    __table_args__ = (
        db.Index('scp_constraint_uk_1', 'subject_policy_id', 'privilege_allowed_id'),
    )

    subject_policy_acl_constraint_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    subject_policy_id = db.Column(db.ForeignKey('subject_policy.subject_policy_id', ondelete='CASCADE'), nullable=False, index=True)
    privilege_allowed_id = db.Column(db.ForeignKey('privilege_allowed.privilege_allowed_id'), nullable=False, index=True)
    grant_scope_id = db.Column(db.ForeignKey('grant_scope.grant_scope_id'), nullable=False, index=True)

    # no backref: special override since fk is part of the pk of SubjectPolicyGrantAllowed
    # https://docs.sqlalchemy.org/en/13/orm/cascades.html
    grant_scope = db.relationship('GrantScope', primaryjoin='SubjectPolicyAclConstraint.grant_scope_id == GrantScope.grant_scope_id')
    privilege_allowed = db.relationship('PrivilegeAllowed', primaryjoin='SubjectPolicyAclConstraint.privilege_allowed_id == PrivilegeAllowed.privilege_allowed_id')
    subject_policy = db.relationship('SubjectPolicy', primaryjoin='SubjectPolicyAclConstraint.subject_policy_id == SubjectPolicy.subject_policy_id')


class SubjectPolicyGrantAllowed(db.Model):
    __tablename__ = 'subject_policy_grant_allowed'

    sp_grant_allowed_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    object_uuid = db.Column(db.String(36), nullable=False)
    object_type = db.Column(db.String(1), nullable=False)
    create_datetime = db.Column(db.DateTime(True), nullable=False, default=datetime.datetime.utcnow)
    subject_policy_acl_constraint_id = db.Column(db.ForeignKey('subject_policy_acl_constraint.subject_policy_acl_constraint_id', ondelete='CASCADE'), nullable=False, index=True)

    subject_policy_acl_constraint = db.relationship('SubjectPolicyAclConstraint', primaryjoin='SubjectPolicyGrantAllowed.subject_policy_acl_constraint_id == SubjectPolicyAclConstraint.subject_policy_acl_constraint_id')


class Subscription(db.Model):
    __tablename__ = 'subscription'
    __table_args__ = (
        db.CheckConstraint("(subscription_state)::text = ANY ((ARRAY['ACTIVE'::character varying, 'PAUSED'::character varying])::text[])"),
        db.Index('uk_subscription', 'subscription_name', 'owner_endpoint_id')
    )

    subscription_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    subscription_uuid = db.Column(db.String(36), nullable=False, unique=True, default=lambda: uuid4())
    subscription_name = db.Column(db.String(30), nullable=False)
    subscription_state = db.Column(db.String(10), nullable=False)
    create_datetime = db.Column(db.DateTime(True), nullable=False, default=datetime.datetime.utcnow)
    owner_endpoint_id = db.Column(db.ForeignKey('endpoint.endpoint_id'), nullable=False, index=True)

    owner_endpoint = db.relationship('Endpoint', primaryjoin='Subscription.owner_endpoint_id == Endpoint.endpoint_id', backref='subscriptions')



class SubscriptionSubject(db.Model):
    __tablename__ = 'subscription_subject'
    __table_args__ = (
        db.CheckConstraint("upper((preferred_fulfillment_type)::text) = ANY (ARRAY['DATA_PUSH'::text, 'DATA_NOTIFY'::text])"),
        db.Index('uk_subscription_subject_1', 'subscription_id', 'subject_id')
    )

    subscription_subject_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    preferred_fulfillment_type = db.Column(db.String(15), nullable=False)
    backing_queue_name = db.Column(db.String(255))
    subject_id = db.Column(db.ForeignKey('subject.subject_id', ondelete='CASCADE'), nullable=False, index=True)
    subscription_id = db.Column(db.ForeignKey('subscription.subscription_id', ondelete='CASCADE'), nullable=False, index=True)

    # no backref
    # https://docs.sqlalchemy.org/en/13/orm/cascades.html
    subject = db.relationship('Subject', primaryjoin='SubscriptionSubject.subject_id == Subject.subject_id')
    subscription = db.relationship('Subscription', primaryjoin='SubscriptionSubject.subscription_id == Subscription.subscription_id')

