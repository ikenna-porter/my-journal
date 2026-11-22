"""api-conventions: validation errors and offset pagination.

No real endpoint validates input yet, so a probe router (test-only) exercises the
shared building blocks: the validation handler and PageParams/Page.
"""

from typing import Annotated

import pytest
from fastapi import APIRouter, Depends, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from app.auth import get_current_user
from app.pagination import Page, PageParams
from tests.conftest import assert_problem


class ProbeBody(BaseModel):
    name: str = Field(min_length=1)


probe = APIRouter(prefix="/api/v1/_probe", dependencies=[Depends(get_current_user)])


@probe.post("/body")
def probe_body(body: ProbeBody) -> dict:
    return {"ok": True}


@probe.get("/items", response_model=Page[int])
def probe_items(params: Annotated[PageParams, Query()]) -> Page[int]:
    items = list(range(45))
    window = items[params.offset : params.offset + params.limit]
    return Page[int](items=window, total=len(items), limit=params.limit, offset=params.offset)


@pytest.fixture
def probe_client(app) -> TestClient:
    app.include_router(probe)
    return TestClient(app)


def test_invalid_body_is_a_validation_problem_listing_fields(probe_client, auth):
    response = probe_client.post("/api/v1/_probe/body", json={"name": ""}, headers=auth)
    body = assert_problem(response, 422, "validation_error")
    assert body["errors"], "errors list must not be empty"
    assert body["errors"][0]["loc"] == ["body", "name"]
    assert isinstance(body["errors"][0]["msg"], str)


def test_auth_is_checked_before_validation(probe_client):
    response = probe_client.post("/api/v1/_probe/body", json={"name": ""})
    assert_problem(response, 401, "unauthenticated")


def test_pagination_defaults(probe_client, auth):
    body = probe_client.get("/api/v1/_probe/items", headers=auth).json()
    assert (body["limit"], body["offset"], body["total"], len(body["items"])) == (20, 0, 45, 20)


def test_second_page(probe_client, auth):
    response = probe_client.get("/api/v1/_probe/items?limit=20&offset=20", headers=auth)
    body = response.json()
    assert (body["limit"], body["offset"], body["total"], len(body["items"])) == (20, 20, 45, 20)


@pytest.mark.parametrize("query", ["limit=0", "limit=101", "limit=500", "offset=-1"])
def test_out_of_range_paging_is_a_validation_problem(probe_client, auth, query):
    response = probe_client.get(f"/api/v1/_probe/items?{query}", headers=auth)
    assert_problem(response, 422, "validation_error")
