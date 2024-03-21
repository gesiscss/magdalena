"""
Read more about conftest.py at https://docs.pytest.org/en/7.1.x/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
"""

import os
import os.path
import uuid

import pytest

from .. import app as magdalena

MAGDALENA_SHARED_DIR = None
MAGDALENA_TMP = None


def pytest_configure(config):
    shared_dir_name = uuid.uuid4().hex
    shared_dir_path = os.path.join("/tmp/", shared_dir_name)

    print("Setting MAGDALENA_SHARED_DIR to %s" % shared_dir_path)
    os.makedirs(shared_dir_path, exist_ok=True)
    MAGDALENA_SHARED_DIR = os.getenv("MAGDALENA_SHARED_DIR", None)
    os.environ["MAGDALENA_SHARED_DIR"] = shared_dir_path

    tmp_dir_name = uuid.uuid4().hex
    tmp_dir_path = os.path.join("/tmp/", tmp_dir_name)

    print("Setting MAGDALENA_TMP to %s" % tmp_dir_path)
    os.makedirs(tmp_dir_path, exist_ok=True)
    MAGDALENA_TMP = os.getenv("MAGDALENA_TMP", None)
    os.environ["MAGDALENA_TMP"] = tmp_dir_path


def pytest_unconfigure(config):
    if MAGDALENA_SHARED_DIR is None:
        os.unsetenv("MAGDALENA_SHARED_DIR")
    else:
        os.putenv("MAGDALENA_SHARED_DIR", MAGDALENA_SHARED_DIR)

    if MAGDALENA_TMP is None:
        os.unsetenv("MAGDALENA_TMP")
    else:
        os.putenv("MAGDALENA_TMP", MAGDALENA_TMP)


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
