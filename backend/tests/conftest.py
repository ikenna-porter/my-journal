import pytest
from fastapi.testclient import TestClient

from app.main import create_app

STUB_TOKEN = "test-token"


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv("AUTH_STUB_TOKEN", STUB_TOKEN)
    monkeypatch.delenv("ENV", raising=False)
    return create_app()


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)


@pytest.fixture
def auth() -> dict[str, str]:
    """Headers for an authenticated request (the slice 0 stub token)."""
    return {"Authorization": f"Bearer {STUB_TOKEN}"}


def assert_problem(response, status: int, code: str) -> dict:
    """Assert an RFC 9457 problem response with our stable `code`, and return its body."""
    assert response.status_code == status, response.text
    assert response.headers["content-type"].startswith("application/problem+json")
    body = response.json()
    assert isinstance(body["type"], str)
    assert isinstance(body["title"], str)
    assert body["status"] == status
    assert isinstance(body["detail"], str)
    assert body["code"] == code
    return body
