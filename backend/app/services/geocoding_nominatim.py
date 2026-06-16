"""Geocoding via Nominatim (OpenStreetMap). Gratuito, con rate-limit.

Richiede uno User-Agent custom (policy d'uso OSM). Testato manualmente,
escluso dalla soglia di copertura perché è codice di rete.
"""

from __future__ import annotations

import httpx

from app.config import Settings
from app.services.interfaces import GeoPoint


class NominatimGeocoder:
    def __init__(self, settings: Settings) -> None:
        self._base = settings.nominatim_base_url
        self._headers = {"User-Agent": settings.user_agent}

    def geocode(self, *, address, city, lat, lon) -> GeoPoint:
        if lat is not None and lon is not None:
            return GeoPoint(lat=lat, lon=lon, display_name=address or city)
        query = ", ".join(p for p in (address, city) if p)
        resp = httpx.get(
            f"{self._base}/search",
            params={"q": query, "format": "json", "limit": 1},
            headers=self._headers,
            timeout=10.0,
        )
        resp.raise_for_status()
        data = resp.json()
        if not data:
            raise ValueError(f"Indirizzo non trovato: {query}")
        first = data[0]
        return GeoPoint(lat=float(first["lat"]), lon=float(first["lon"]), display_name=first.get("display_name"))
