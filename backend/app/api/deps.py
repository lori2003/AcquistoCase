"""Dependency injection: costruisce i servizi reali dalle env var.

Nei test questa dipendenza viene sovrascritta con servizi fake
(`app.dependency_overrides`), quindi qui vive solo il wiring di produzione.
"""

from __future__ import annotations

from functools import lru_cache

from app.config import get_settings
from app.services.ai_openrouter import OpenRouterReporter
from app.services.amenities_overpass import OverpassAmenityProvider
from app.services.geocoding_nominatim import NominatimGeocoder
from app.services.market_omi import OmiCsvProvider
from app.services.orchestrator import EvaluationService


@lru_cache
def get_evaluation_service() -> EvaluationService:
    settings = get_settings()
    return EvaluationService(
        geocoder=NominatimGeocoder(settings),
        amenities=OverpassAmenityProvider(settings),
        market=OmiCsvProvider(),
        ai=OpenRouterReporter(settings),
    )
