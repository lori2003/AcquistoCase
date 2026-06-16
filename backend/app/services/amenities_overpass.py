"""Servizi vicini via Overpass API (OpenStreetMap). Gratuito, con rate-limit.

Per l'MVP la distanza è in linea d'aria convertita in minuti a piedi; un upgrade
naturale è il routing reale con OSMnx. Escluso dalla soglia di copertura.
"""

from __future__ import annotations

import math

import httpx

from app.config import Settings
from app.core.decay import walk_minutes
from app.models.output import AmenityHit
from app.services.interfaces import GeoPoint

# Mappa categoria interna -> filtro Overpass (tag OSM)
OSM_FILTERS: dict[str, str] = {
    "metro": '[railway=station][station=subway]',
    "public_transport": '[highway=bus_stop]',
    "supermarket": '[shop=supermarket]',
    "school": '[amenity=school]',
    "bar": '[amenity=bar]',
    "restaurant": '[amenity=restaurant]',
    "park": '[leisure=park]',
}


def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


class OverpassAmenityProvider:
    def __init__(self, settings: Settings) -> None:
        self._url = settings.overpass_base_url
        self._headers = {"User-Agent": settings.user_agent}

    def nearest_by_category(self, point: GeoPoint, categories, radius_m: int = 1500):
        result: dict[str, AmenityHit | None] = {}
        for cat in categories:
            if cat == "center":
                # Il "centro" richiede un dato dedicato; non gestito in questo MVP.
                result[cat] = None
                continue
            osm_filter = OSM_FILTERS.get(cat)
            if osm_filter is None:
                result[cat] = None
                continue
            result[cat] = self._nearest(point, cat, osm_filter, radius_m)
        return result

    def _nearest(self, point, category, osm_filter, radius_m) -> AmenityHit | None:
        query = (
            f"[out:json][timeout:25];"
            f"node{osm_filter}(around:{radius_m},{point.lat},{point.lon});"
            f"out body 30;"
        )
        resp = httpx.post(self._url, data=query, headers=self._headers, timeout=30.0)
        resp.raise_for_status()
        elements = resp.json().get("elements", [])
        if not elements:
            return None
        best = min(elements, key=lambda e: _haversine_m(point.lat, point.lon, e["lat"], e["lon"]))
        dist = _haversine_m(point.lat, point.lon, best["lat"], best["lon"])
        return AmenityHit(
            category=category,
            name=best.get("tags", {}).get("name"),
            walk_minutes=round(walk_minutes(dist), 1),
            distance_m=round(dist, 1),
        )
