import os
from pathlib import Path

import pytest
from sqlalchemy.orm import sessionmaker

pth = Path(__file__).parent
os.environ["FIXTURE_DIR"] = str(pth / "fixtures")
os.environ["ENV_FILE"] = str(pth / "fixtures/dev_env_file")


@pytest.fixture(scope="session")
def db():
    from uudex_server.app.db import get_db

    yield get_db()


import pytest
from sqlmodel import Session, SQLModel, create_engine
import uudex_server.models as m
import uudex_server.repos as r    # Import for repository functions
from pathlib import Path

# Replace 'sqlite:///:memory:' with your actual database URL if required
DATABASE_URL = 'sqlite:///:memory:'


# DB_PATH='/home/os2204/repos/UUDEX/fastapi-web-server/test-db.sqlite'
# Path(DB_PATH).unlink(missing_ok=True)
# DATABASE_URL = f'sqlite:///{DB_PATH}'
@pytest.fixture(name="session", scope="function")
def fixture_session():
    engine = create_engine(DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


# Set up an SQLite in-memory database
@pytest.fixture(scope="function")
def sqlite_test_engine():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)    # Generate schema
    yield engine
    engine.dispose()


@pytest.fixture(name="api_session", scope="function")
def api_session_fixture(sqlite_test_engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_test_engine)
    with SessionLocal() as session:
        SQLModel.metadata.create_all(bind=session.bind)
        # Seed data in the correct order to respect relationships.
        create_participants(session)    # Essential for many other tables
        create_auth_groups(session)    # Independent
        create_auth_roles(session)    # Independent
        create_privileges(session)    # Needed for Subject ACL
        create_privilege_allowed(session)    # Needed for Subject Policy ACL Constraints
        create_data_types(session)    # Needed for DataType History and Attached DataTypes
        create_dataset_definitions(session)    # Necessary for Subjects
        create_contacts(session)    # Follows Participants
        create_data_type_history(session)    # Follows Data Types
        create_endpoints(session)    # Follows Participants
        create_subjects(session)    # After Dataset Definitions
        create_datasets(session)    # Follows Participants, Subject
        create_grant_scopes(session)    # Before Subject ACL, Subject Policy ACL Constraints
        create_attached_data_types(session)    # After Data Types and Dataset Definitions
        create_subject_acls(session)    # After Subjects, Privileges, Grant Scopes
        create_subject_acl_grants(session)    # After Subject ACLs
        create_subject_policies(session)    # After Grant Scopes
        create_subject_policy_acl_constraints(session)    # After Subject Policies
        create_subject_policy_grant_allowed(session)    # After Subject Policy ACL Constraints
        create_subscriptions(session)    # After EndPoints
        create_subscription_subjects(session)    # After Subjects, Subscriptions
        yield session
        session.rollback()


@pytest.fixture(name="subject_repo")
def subject_repo_fixture(session: Session):
    return r.SubjectRepository(session)


@pytest.fixture(name="participant_repo")
def participant_repo_fixture(session: Session):
    return r.ParticipantRepository(session)


@pytest.fixture(name="dataset_repo")
def dataset_repo_fixture(session: Session):
    return r.DatasetRepository(session)


@pytest.fixture(name="dataset_definition_repo")
def dataset_definition_repo_fixture(session: Session):
    return r.DatasetDefinitionRepository(session)


@pytest.fixture(name="data_type_repo")
def data_type_repo_fixture(session: Session):
    return r.DataTypeRepository(session)


@pytest.fixture(name="attached_data_type_repo")
def attached_data_type_repo_fixture(session: Session):
    return r.AttachedDataTypeRepository(session)


@pytest.fixture(name="endpoint_repo")
def endpoint_repo_fixture(session: Session):
    return r.EndpointRepository(session)


@pytest.fixture(name="subscription_repo")
def subscription_repo_fixture(session: Session):
    return r.SubscriptionRepository(session)


@pytest.fixture(name="subject_policy_repo")
def subject_policy_repo_fixture(session: Session):
    return r.SubjectPolicyRepository(session)


@pytest.fixture(name="subscription_subject_repo")
def subscription_subject_repo_fixture(session: Session):
    return r.SubscriptionSubjectRepository(session)


@pytest.fixture(name="participant_visibility_repo")
def participant_visibility_repo_fixture(session: Session):
    return r.ParticipantVisibilityRepository(session)


@pytest.fixture(name="grand_scope_repo")
def grant_scope_repo_fixture(session: Session):
    return r.GrantScopeRepository(session)


@pytest.fixture(name="subject_acl_repo")
def subject_acl_repo_fixture(session: Session):
    return r.SubjectAclRepository(session)


@pytest.fixture(name="subject_acl_grant_repo")
def subject_acl_grant_repo_fixture(session: Session):
    return r.SubjectAclGrantRepository(session)


@pytest.fixture(name="subject_policy_acl_constraint_repo")
def subject_policy_acl_constraint_repo_fixture(session: Session):
    return r.SubjectPolicyAclConstraintRepository(session)


@pytest.fixture(name="subject_policy_grant_allowed_repo")
def subject_policy_grant_allowed_repo_fixture(session: Session):
    return r.SubjectPolicyGrantAllowedRepository(session)


@pytest.fixture(name="authenticated_user")
def fixture_authenticated_user():
    # Mock authenticated user, adjust accordingly
    return m.AuthenticatedUser(endpoint=m.EndPoint(participant_id=1, endpoint_id=1))


###########################################################################################################
#### Creation functions for seeding the database before running tests.
###########################################################################################################
from datetime import datetime


def create_auth_groups(api_session: Session):
    group1 = m.AuthGroup(group_uuid="group-uuid-1",
                         group_name="Admin Group",
                         description="Group for administration",
                         created_datetime=datetime.now())
    api_session.add(group1)
    api_session.commit()


def create_auth_roles(api_session: Session):
    role1 = m.AuthRole(role_uuid="role-uuid-1",
                       role_name="Admin Role",
                       description="Role for admins",
                       created_datetime=datetime.now())
    api_session.add(role1)
    api_session.commit()


def create_data_types(api_session: Session):
    # Every field that is non-nullable or serving a constraint must be populated
    data_type1 = m.DataType(
        data_type_uuid="uuid-dt-1",
        data_type_name="Type1",
        description="Description for Type1",
        schema_definition="{}",    # Assume this is an empty JSON schema example
        specification_reference="Standard Reference"    # Ensure this string is not None
    )
    api_session.add(data_type1)
    api_session.commit()


def create_dataset_definitions(api_session: Session):
    dataset_def1 = m.DatasetDefinition(dataset_definition_uuid="uuid-dd-1",
                                       dataset_definition_name="DatasetDef1",
                                       description="Dataset definition description",
                                       create_datetime=datetime.now())
    api_session.add(dataset_def1)
    api_session.commit()


def create_grant_scopes(api_session: Session):
    grant_scope1 = m.GrantScope(grant_scope_name="ALLOW_ALL")
    api_session.add(grant_scope1)
    api_session.commit()


def create_privileges(api_session: Session):
    privilege1 = m.Privilege(privilege_name="PUBLISH")
    privilege2 = m.Privilege(privilege_name="SUBSCRIBE")
    api_session.add_all([privilege1, privilege2])
    api_session.commit()


def create_privilege_allowed(api_session: Session):
    priv_allowed1 = m.PrivilegeAllowed(privilege_allowed_name="ALLOW_PUBLISH")
    api_session.add(priv_allowed1)
    api_session.commit()


def create_participants(api_session: Session):
    participant1 = m.Participant(participant_uuid="participant-uuid-1",
                                 participant_short_name="Part1",
                                 participant_long_name="Participant 1",
                                 description="First test participant",
                                 root_org_sw='Y',
                                 active_sw='Y',
                                 create_datetime=datetime.now())
    participant2 = m.Participant(participant_uuid="participant-uuid-2",
                                 participant_short_name="Part2",
                                 participant_long_name="Participant 2",
                                 description="Second test participant",
                                 root_org_sw='Y',
                                 active_sw='N',
                                 create_datetime=datetime.now())
    api_session.add_all([participant1, participant2])
    api_session.commit()


def create_contacts(api_session: Session):
    contact1 = m.Contact(contact_name="Test User", contact_number="123-456-7890", participant_id=1)
    api_session.add(contact1)
    api_session.commit()


def create_data_type_history(api_session: Session):
    history1 = m.DataTypeHistory(data_type_id=1,
                                 create_datetime=datetime.now(),
                                 description="Initial version",
                                 schema_definition="{}",
                                 version_number=1)
    api_session.add(history1)
    api_session.commit()


def create_endpoints(api_session: Session):
    endpoint1 = m.EndPoint(endpoint_uuid="endpoint-uuid-1",
                           endpoint_user_name="user1",
                           certificate_dn="CN=Test User",
                           description="Endpoint for Test User",
                           active_sw='Y',
                           uudex_administrator_sw='N',
                           participant_administrator_sw='N',
                           create_datetime=datetime.now(),
                           participant_id=1)
    api_session.add(endpoint1)
    api_session.commit()


def create_participant_visibility(api_session: Session):
    visibility = m.ParticipantVisibility(exposed_by_participant_id=1,
                                         exposed_to_participant_id=2,
                                         create_datetime=datetime.now())
    api_session.add(visibility)
    api_session.commit()


def create_subjects(api_session: Session):
    subject1 = m.Subject(
        subject_uuid="uuid-s-1",
        subject_name="Subject1",
        dataset_instance_key="key1",
        subscription_type="EVENT",
        fulfillment_types_available="DATA_PUSH",
        backing_exchange_name="ExchangeName",    # Provide a value for backing_exchange_name
        create_datetime=datetime.now(),
        owner_participant_id=1,
        dataset_definition_id=1)
    api_session.add(subject1)
    api_session.commit()


def create_subject_acls(api_session: Session):
    acl1 = m.SubjectAcl(subject_id=1, privilege_id=1, grant_scope_id=1)
    api_session.add(acl1)
    api_session.commit()


def create_subject_acl_grants(api_session: Session):
    acl_grant1 = m.SubjectAclGrant(subject_acl_id=1,
                                   participant_id=1,
                                   create_datetime=datetime.now())
    api_session.add(acl_grant1)
    api_session.commit()


def create_subject_policies(api_session: Session):
    policy = m.SubjectPolicy(
        subject_policy_uuid="uuid-pol-1",
        subject_policy_type="PARTICIPANT",
        subject_policy_type_sort=1,
        action="ALLOW",
        full_queue_behavior="BLOCK_NEW",    # Provide a valid behavior setting
        max_queue_size_kb=1024,    # Example value, replace with appropriate or default as needed
        max_message_count=100,    # Example value
        max_priority=10,    # Example value
        target_participant_id=1,    # Ensure this corresponds to an existing participant
        dataset_definition_id=1    # Ensure this exists in your seed data
    )
    api_session.add(policy)
    api_session.commit()


def create_subject_policy_acl_constraints(api_session: Session):
    acl_constraint1 = m.SubjectPolicyAclConstraint(
        subject_policy_id=1,    # Reference an existing subject policy
        privilege_allowed_id=1,    # Privilege Allowed Reference
        grant_scope_id=1    # Grant Scope Reference
    )
    api_session.add(acl_constraint1)
    api_session.commit()


def create_subject_policy_grant_allowed(api_session: Session):
    grant_allowed = m.SubjectPolicyGrantAllowed(subject_policy_acl_constraint_id=1,
                                                participant_id=1,
                                                create_datetime=datetime.now())
    api_session.add(grant_allowed)
    api_session.commit()


def create_subscriptions(api_session: Session):
    subscription1 = m.Subscription(subscription_uuid="sub-uuid-1",
                                   subscription_name="TestSubscription",
                                   subscription_state="ACTIVE",
                                   create_datetime=datetime.now(),
                                   owner_endpoint_id=1)
    api_session.add(subscription1)
    api_session.commit()


def create_subscription_subjects(api_session: Session):
    subscription_subject1 = m.SubscriptionSubject(
        preferred_fulfillment_type="DATA_PUSH",
        backing_queue_name="Queue1",    # Provide a non-nullable value
        subject_id=1,    # Ensure this is an existing subject
        subscription_id=1    # Ensure this is an existing subscription
    )
    api_session.add(subscription_subject1)
    api_session.commit()


def create_datasets(api_session: Session):
    dataset1 = m.Dataset(dataset_uuid="dataset-uuid-1",
                         dataset_name="Test Dataset",
                         description="A dataset for testing",
                         properties="{}",
                         payload=b'',
                         payload_size=0,
                         payload_md5_hash='md5hash',
                         payload_compression_algorithm="NONE",
                         version_number=1,
                         create_datetime=datetime.now(),
                         owner_participant_id=1,
                         subject_id=1)
    api_session.add(dataset1)
    api_session.commit()


def create_attached_data_types(api_session: Session):
    attached_data_type = m.AttachedDataType(data_type_id=1,
                                            dataset_definition_id=1,
                                            create_datetime=datetime.now())
    api_session.add(attached_data_type)
    api_session.commit()
