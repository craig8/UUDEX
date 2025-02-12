import os
import sys
import pytest

# Add the package root directory to Python path
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def pytest_addoption(parser):
    parser.addoption(
        "--use-real-server",
        action="store_true",
        default=False,
        help="Run tests against real UUDEX server instead of mock")


@pytest.fixture
def use_real_server(request):
    return request.config.getoption("--use-real-server")
