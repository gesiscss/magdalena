"""
Read more about conftest.py at https://docs.pytest.org/en/7.1.x/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
"""

import os
import os.path
import uuid

import pytest

from .. import app as magdalena

MAGDALENA_SHARED_DIR = None


def pytest_configure(config):
    dir_name = uuid.uuid4().hex
    dir_path = os.path.join("/tmp/", dir_name)
    os.makedirs(dir_path, exist_ok=True)
    MAGDALENA_SHARED_DIR = os.getenv("MAGDALENA_SHARED_DIR", None)
    os.environ["MAGDALENA_SHARED_DIR"] = dir_path


def pytest_unconfigure(config):
    if MAGDALENA_SHARED_DIR is None:
        os.unsetenv("MAGDALENA_SHARED_DIR")
    else:
        os.putenv("MAGDALENA_SHARED_DIR", MAGDALENA_SHARED_DIR)


@pytest.fixture()
def app():
    app = magdalena.app
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
