"""Deduplica (funzioni pure): unisce annunci che descrivono lo stesso immobile.

Due annunci sono lo stesso immobile se prezzo e mq coincidono (entro tolleranza) e
le coordinate sono vicine; in assenza di coordinate si ripiega sulla stessa città.
Quando sono duplicati, si conserva un solo annuncio e si unisce la lista `sources`.
"""

from __future__ import annotations

import math

from app.models.listing import Listing


def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _within_pct(a: float, b: float, tol_pct: float) -> bool:
    if a == 0 and b == 0:
        return True
    ref = max(abs(a), abs(b))
    return abs(a - b) / ref * 100.0 <= tol_pct


def same_property(
    a: Listing,
    b: Listing,
    price_tol_pct: float = 2.0,
    mq_tol_pct: float = 3.0,
    max_dist_m: float = 75.0,
) -> bool:
    if not _within_pct(a.price_eur, b.price_eur, price_tol_pct):
        return False
    if not _within_pct(a.mq, b.mq, mq_tol_pct):
        return False
    if None not in (a.lat, a.lon, b.lat, b.lon):
        return _haversine_m(a.lat, a.lon, b.lat, b.lon) <= max_dist_m
    return a.city.strip().lower() == b.city.strip().lower()


def _merge(primary: Listing, other: Listing) -> Listing:
    merged_sources = list(dict.fromkeys([*primary.sources, *other.sources]))
    data = primary.model_dump()
    data["sources"] = merged_sources
    # completa i campi mancanti del primario con quelli dell'altra sorgente
    for field in ("address", "lat", "lon", "image_url", "rooms", "title", "url"):
        if data.get(field) in (None, "") and getattr(other, field) not in (None, ""):
            data[field] = getattr(other, field)
    return Listing(**data)


def deduplicate(listings: list[Listing]) -> list[Listing]:
    """Unisce i duplicati preservando l'ordine di prima apparizione."""
    result: list[Listing] = []
    for listing in listings:
        match_index = next(
            (i for i, kept in enumerate(result) if same_property(kept, listing)), None
        )
        if match_index is None:
            result.append(listing)
        else:
            result[match_index] = _merge(result[match_index], listing)
    return result
