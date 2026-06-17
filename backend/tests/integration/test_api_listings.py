from fastapi.testclient import TestClient

from app.api.deps import get_aggregator_service
from app.main import app
from app.services.aggregator import AggregatorService
from tests.fakes.fake_services import FakeListingSource


def _client(sources):
    service = AggregatorService(sources=sources)
    app.dependency_overrides[get_aggregator_service] = lambda: service
    return TestClient(app)


def test_listings_endpoint_returns_deduped(monkeypatch):
    sources = [
        FakeListingSource("immobiliare", [
            {"prezzo_vendita": 250000, "superficie": 80, "citta": "Milano", "latitudine": 45.4655, "longitudine": 9.1715},
        ]),
        FakeListingSource("idealista", [
            {"price": 251000, "size": 80, "city": "Milano", "lat": 45.4655, "lng": 9.1715},
        ]),
    ]
    client = _client(sources)
    try:
        resp = client.get("/api/listings", params={"city": "Milano"})
        assert resp.status_code == 200
        body = resp.json()
        assert len(body) == 1
        assert set(body[0]["sources"]) == {"immobiliare", "idealista"}
    finally:
        app.dependency_overrides.clear()


def test_listings_requires_city():
    client = _client([FakeListingSource("a", [])])
    try:
        resp = client.get("/api/listings")
        assert resp.status_code == 422
    finally:
        app.dependency_overrides.clear()
