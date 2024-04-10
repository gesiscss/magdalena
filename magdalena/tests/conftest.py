# SPDX-FileCopyrightText: 2023 - 2024 GESIS - Leibniz-Institut für Sozialwissenschaften
# SPDX-FileContributor: Raniere Gaia Costa da Silva <Raniere.CostadaSilva@gesis.org>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Read more about conftest.py at https://docs.pytest.org/en/7.1.x/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
"""

import os
import os.path
import uuid

import pytest
from pytest import MonkeyPatch

os.environ["MYBINDER_URL"] = "https://notebooks.gesis.org/binder"
os.environ["KEYCLOAK_SCHEME"] = "http"
os.environ["KEYCLOAK_DOMAIN"] = "localhost"
os.environ["KEYCLOAK_REALM"] = "pytest"
os.environ["JWT_ISSUER"] = "http://localhost/realms/pytest"

from .. import pem

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

    os.unsetenv("KEYCLOAK_SCHEME")
    os.unsetenv("KEYCLOAK_DOMAIN")
    os.unsetenv("KEYCLOAK_REALM")
    os.unsetenv("JWT_ISSUER")


@pytest.fixture()
def app():
    with MonkeyPatch.context() as mp:
        mp.setattr(pem, "KEYCLOAK_ISSUER", lambda: "http://localhost/realms/pytest")
        mp.setattr(
            pem,
            "retrieve_public_key",
            lambda: """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAwN85IuBtAfXIcstWVBtr
X64AD2BdKJVDnR7uJSt+E49p8Acr4zt9rbpHpz+rQgXJGnYXZ/zOfUBmW44ZIHWl
2sDnfHHaNcmC1zk1Z7iwxd0tIvFDY3C0qoQ4l8FhbDnxIxU2rp2oLLc5ws3hrbQA
g4ArBB4RxN06mj/F4v0lteiB08wvQPHxd3UnYCPZGrWSLSN0nLqNx7r/pBGrwMX4
UDZVEA7PCv3amDsWcTShyIteFQvXS3E3qXOepLB3DdzzdeNKqmubDC5TkomJ7SJu
PRLdec6vSwb0sAGBPu5JYXstkVuS41jHuhM9c7Wm0cgMj59OXydnhqm83Z+NLIWc
kFOMQ4/0YEKXCacvC45pZrM5Mwn8b2FSnIjcPJI6pfQIqLUco0pdgPS2urswP776
OaukTOHjT46bIYEtoFg/XVasMfhZCFjU/b6Qf2pGgz8Lvj5tkxmHWFXYcF+ZXbbH
bnIQvXAef0BSKhM1s1nRgmxw7osy1HKKYREy+TZqbIfv8EkV/yeJQZPCVDVDGYs1
AVA7+7wLkAmQDJw6P4MnKRnmAVwosemlr5v/PgNcxsQku8eoDnOKJBbr0r7pivKc
WPymBa1m5W/tVCwnpfukgutV2w8OqqO2e6yPFlnMANvk+b8CKsZ305bd0xwvi8+3
lZHFhEiyaYv9p7cHNWykBvMCAwEAAQ==
-----END PUBLIC KEY-----""",
        )

        from .. import app as magdalena

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
