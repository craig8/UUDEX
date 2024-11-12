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
import uudex_server.repos as repo    # Import for repository functions
from pathlib import Path

# Replace 'sqlite:///:memory:' with your actual database URL if required
DATABASE_URL = 'sqlite:///:memory:'

#DB_PATH='/home/os2204/repos/UUDEX/fastapi-web-server/test-db.sqlite'
#Path(DB_PATH).unlink(missing_ok=True)
#DATABASE_URL = f'sqlite:///{DB_PATH}'


@pytest.fixture(name="session")
def fixture_session():
    engine = create_engine(DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="authenticated_user")
def fixture_authenticated_user():
    # Mock authenticated user, adjust accordingly
    return m.AuthenticatedUser(endpoint=m.EndPoint(participant_id=1, endpoint_id=1))
