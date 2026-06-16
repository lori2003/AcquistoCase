"""Interfacce (Protocol) verso i servizi esterni.

La logica `core` non dipende da queste: l'orchestrator riceve le implementazioni
via costruttore, così i test iniettano dei fake e non toccano mai la rete.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from app.models.output import AmenityHit


@dataclass(frozen=True)
class GeoPoint:
    lat: float
    lon: float
    display_name: str | None = None


@dataclass(frozen=True)
class OmiRange:
    min_per_mq: float | None
    max_per_mq: float | None


@dataclass(frozen=True)
class AIResult:
    ok: bool
    text: str | None


@runtime_checkable
class Geocoder(Protocol):
    def geocode(
        self, *, address: str | None, city: str, lat: float | None, lon: float | None
    ) -> GeoPoint: ...


@runtime_checkable
class AmenityProvider(Protocol):
    def nearest_by_category(
        self, point: GeoPoint, categories: list[str], radius_m: int = 1500
    ) -> dict[str, AmenityHit | None]: ...


@runtime_checkable
class MarketPriceProvider(Protocol):
    def omi_range(self, city: str, zone: str | None) -> OmiRange: ...


@runtime_checkable
class AIReporter(Protocol):
    def write_report(self, structured: dict) -> AIResult: ...
