"""Dependency injection: costruisce i servizi reali dalle env var.

Nei test questa dipendenza viene sovrascritta con servizi fake
(`app.dependency_overrides`), quindi qui vive solo il wiring di produzione.
"""

from __future__ import annotations

from functools import lru_cache

from app.config import get_settings
from app.services.aggregator import AggregatorService
from app.services.ai_openrouter import OpenRouterReporter
from app.services.amenities_overpass import OverpassAmenityProvider
from app.services.geocoding_nominatim import NominatimGeocoder
from app.services.listing_sources import SampleListingSource
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


@lru_cache
def get_aggregator_service() -> AggregatorService:
    # Sorgenti di esempio (feed autorizzati / dati demo). Per collegare una fonte
    # reale, sostituisci con un'implementazione di ListingSource su API ufficiale.
    return AggregatorService(
        sources=[
            SampleListingSource("immobiliare", "listings_immobiliare.json"),
            SampleListingSource("idealista", "listings_idealista.json"),
        ]
    )
