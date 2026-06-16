"""Fixture condivise: servizi fake, orchestrator e TestClient con override."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_evaluation_service
from app.main import app
from app.services.orchestrator import EvaluationService
from tests.fakes.fake_services import (
    FakeAIReporter,
    FakeAmenityProvider,
    FakeGeocoder,
    FakeMarketPriceProvider,
)


@pytest.fixture
def amenity_minutes():
    return {"metro": 5.0, "public_transport": 5.0, "supermarket": 5.0,
            "school": 10.0, "bar": 5.0, "restaurant": 5.0, "park": 10.0}


@pytest.fixture
def make_service():
    def _make(*, amenities=None, omi_min=2000.0, omi_max=3000.0, ai_fail=False):
        return EvaluationService(
            geocoder=FakeGeocoder(),
            amenities=FakeAmenityProvider(amenities or {}),
            market=FakeMarketPriceProvider(omi_min=omi_min, omi_max=omi_max),
            ai=FakeAIReporter(should_fail=ai_fail),
        )
    return _make


@pytest.fixture
def client(make_service):
    """TestClient con la dipendenza del servizio sovrascritta da fake (no rete)."""
    service = make_service(
        amenities={"metro": 5.0, "supermarket": 5.0, "bar": 5.0, "restaurant": 5.0},
    )
    app.dependency_overrides[get_evaluation_service] = lambda: service
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def valid_payload():
    return {
        "property": {
            "city": "Milano",
            "address": "Via Roma 1",
            "budget_eur": 300000,
            "price_eur": 200000,
            "mq": 80,
        },
        "objective": "near_metro",
        "preferences": {"metro": 1.0, "bar": 0.5},
    }
