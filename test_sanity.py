import pytest
from flask import Response
from flask.testing import FlaskClient

from factory import create_app


@pytest.fixture
def client():
    f = create_app()
    with f.test_client() as client:
        with f.app_context():
            pass
        yield client


def test_home(client: FlaskClient):
    response: Response = client.get('/')
    assert response.status_code == 200
    assert b'Lorem ipsum' in response.data
