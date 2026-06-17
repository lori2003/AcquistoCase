"""Aggregatore multi-sorgente: Worker -> Transformer -> Deduplica.

Sottile: la logica vera (normalizzazione, deduplica) sta in `app.core`.
"""

from __future__ import annotations

from app.core.dedup import deduplicate
from app.core.normalize import normalize_many
from app.models.listing import Listing
from app.services.listing_sources import ListingSource


class AggregatorService:
    def __init__(self, sources: list[ListingSource]) -> None:
        self.sources = sources

    def aggregate(self, city: str) -> list[Listing]:
        normalized: list[Listing] = []
        for source in self.sources:
            normalized.extend(normalize_many(source.fetch(city), source.name))
        deduped = deduplicate(normalized)
        return sorted(deduped, key=lambda x: x.price_per_mq)
