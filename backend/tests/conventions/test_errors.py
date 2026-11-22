"""api-conventions: Problem details error format."""

from tests.conftest import assert_problem

REQUIRED_CODES = {
    "unauthenticated",
    "not_found",
    "validation_error",
    "method_not_allowed",
    "conflict",
    "conversation_expired",
    "spend_limit_reached",
    "not_implemented",
}


def test_unknown_route_is_a_not_found_problem(client):
    assert_problem(client.get("/api/v1/does-not-exist"), 404, "not_found")


def test_wrong_method_is_a_method_not_allowed_problem(client):
    assert_problem(client.delete("/api/v1/health"), 405, "method_not_allowed")


def _resolve(schema: dict, components: dict) -> dict:
    ref = schema.get("$ref")
    return components[ref.rsplit("/", 1)[-1]] if ref else schema


def test_contract_enumerates_every_error_code(app):
    """The generated contract lists every allowed `code` as an enum on the problem schema."""
    components = app.openapi()["components"]["schemas"]
    enums = []
    for schema in components.values():
        code = schema.get("properties", {}).get("code")
        if code:
            enums.append(set(_resolve(code, components).get("enum", [])))
    assert any(REQUIRED_CODES <= enum for enum in enums), enums
