"""Implementazioni in-memory delle interfacce dei servizi, per i test.

Nessuna chiamata di rete: ogni comportamento è configurabile dal test.
"""

from __future__ import annotations

from app.models.output import AmenityHit
from app.services.interfaces import AIResult, GeoPoint, OmiRange


class FakeGeocoder:
    def __init__(self, point: GeoPoint | None = None) -> None:
        self.point = point or GeoPoint(lat=45.4642, lon=9.19, display_name="Milano")

    def geocode(self, *, address, city, lat, lon) -> GeoPoint:
        return self.point


class FakeAmenityProvider:
    def __init__(self, minutes_by_category: dict[str, float] | None = None) -> None:
        # category -> walking minutes; categorie assenti = non trovate (None)
        self.minutes_by_category = minutes_by_category or {}

    def nearest_by_category(self, point, categories, radius_m: int = 1500):
        result: dict[str, AmenityHit | None] = {}
        for cat in categories:
            mins = self.minutes_by_category.get(cat)
            if mins is None:
                result[cat] = None
            else:
                result[cat] = AmenityHit(
                    category=cat, name=f"{cat} di prova", walk_minutes=mins, distance_m=mins * 80.0
                )
        return result


class FakeMarketPriceProvider:
    def __init__(self, omi_min: float | None = 2000.0, omi_max: float | None = 3000.0) -> None:
        self.omi_min = omi_min
        self.omi_max = omi_max

    def omi_range(self, city, zone) -> OmiRange:
        return OmiRange(min_per_mq=self.omi_min, max_per_mq=self.omi_max)


class FakeListingSource:
    def __init__(self, name: str, raws: list[dict]) -> None:
        self.name = name
        self._raws = raws

    def fetch(self, city: str) -> list[dict]:
        return list(self._raws)


class FakeAIReporter:
    def __init__(self, should_fail: bool = False, text: str = "Report AI di prova.") -> None:
        self.should_fail = should_fail
        self.text = text

    def write_report(self, structured: dict) -> AIResult:
        if self.should_fail:
            return AIResult(ok=False, text=None)
        return AIResult(ok=True, text=self.text)
