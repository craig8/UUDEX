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
    

