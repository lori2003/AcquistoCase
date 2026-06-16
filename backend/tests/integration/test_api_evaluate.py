def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_evaluate_happy_path(client, valid_payload):
    resp = client.post("/api/evaluate", json=valid_payload)
    assert resp.status_code == 200
    body = resp.json()
    assert 0 <= body["final_score"] <= 100
    assert set(body["components"]) == {"price_score", "distance_score", "services_score", "objective_score"}
    assert isinstance(body["data_risks"], list)
    assert isinstance(body["suggestions"], list)


def test_evaluate_rejects_zero_mq(client, valid_payload):
    valid_payload["property"]["mq"] = 0
    resp = client.post("/api/evaluate", json=valid_payload)
    assert resp.status_code == 422


def test_evaluate_rejects_missing_location(client, valid_payload):
    valid_payload["property"].pop("address")
    resp = client.post("/api/evaluate", json=valid_payload)
    assert resp.status_code == 422


def test_evaluate_with_ai_down_still_200(make_service, valid_payload):
    from app.api.deps import get_evaluation_service
    from app.main import app
    from fastapi.testclient import TestClient

    service = make_service(amenities={"metro": 5.0}, ai_fail=True)
    app.dependency_overrides[get_evaluation_service] = lambda: service
    try:
        resp = TestClient(app).post("/api/evaluate", json=valid_payload)
        assert resp.status_code == 200
        assert any(r["code"] == "AI_UNAVAILABLE" for r in resp.json()["data_risks"])
    finally:
        app.dependency_overrides.clear()
