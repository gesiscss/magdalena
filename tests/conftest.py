import pytest

from .. import app as magdalena

@pytest.fixture()
def app():
    app = magdalena.app
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
