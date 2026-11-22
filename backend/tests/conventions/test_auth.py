"""api-conventions: Bearer authentication, Current user, Unbuilt endpoints."""

import pytest

from app.main import create_app
from tests.conftest import assert_problem


def test_missing_token_is_unauthenticated(client):
    assert_problem(client.get("/api/v1/me"), 401, "unauthenticated")


def test_invalid_token_is_unauthenticated(client):
    response = client.get("/api/v1/me", headers={"Authorization": "Bearer wrong"})
    assert_problem(response, 401, "unauthenticated")


def test_non_bearer_scheme_is_unauthenticated(client):
    response = client.get("/api/v1/me", headers={"Authorization": "Basic dXNlcjpwYXNz"})
    assert_problem(response, 401, "unauthenticated")


def test_me_with_stub_token_is_not_implemented(client, auth):
    assert_problem(client.get("/api/v1/me", headers=auth), 501, "not_implemented")


def test_stub_token_refused_in_production(monkeypatch):
    monkeypatch.setenv("AUTH_STUB_TOKEN", "anything")
    monkeypatch.setenv("ENV", "production")
    with pytest.raises(RuntimeError, match="AUTH_STUB_TOKEN"):
        create_app()
