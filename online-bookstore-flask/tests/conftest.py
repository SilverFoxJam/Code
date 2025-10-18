# tests/conftest.py
import pytest
from wsgi import app as flask_app  # use the robust shim

@pytest.fixture(scope="session")
def app():
    return flask_app

@pytest.fixture()
def client(app):
    return app.test_client()
