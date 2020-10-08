from flask import Response
from flask.testing import FlaskClient


def test_home(client: FlaskClient):
    response: Response = client.get("/")
    assert response.status_code == 200
    assert b"Lorem ipsum" in response.data
