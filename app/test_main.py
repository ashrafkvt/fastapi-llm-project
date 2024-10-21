import pytest

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


@pytest.fixture(scope="module")
def celery_app():
    from app.tasks import app as celery_app
    return celery_app
