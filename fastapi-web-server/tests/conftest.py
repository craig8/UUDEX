import os
from pathlib import Path

import pytest

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


#DB_PATH='/home/os2204/repos/UUDEX/fastapi-web-server/test-db.sqlite'
#Path(DB_PATH).unlink(missing_ok=True)
#DATABASE_URL = f'sqlite:///{DB_PATH}'
@pytest.fixture(name="session", scope="function")
def fixture_session():
    engine = create_engine(DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


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
